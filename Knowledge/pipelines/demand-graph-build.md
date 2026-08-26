---
type: pipeline
pipeline: Demand Graph build (search terms → published concept graph)
date: 2026-08-26
purpose: turn a raw Amazon search-term export into a versioned, measured, published demand hierarchy with trend and product layers attached
cadence: per major version (v1 2026-08-19, v4/v4.1 2026-08-20); re-run on new data releases
sources:
  - Mantis4Retail-Repo:Mantis4Retail/analysis/demand-graph/ (branch diego/demand-graph-explorer — pipeline/step0–step9, validation.py, README.md)
  - Mantis4Retail-Repo:Mantis4Retail/analysis/demand-graph/docs/PROJECT_CHRONICLE.md
  - ~/DemandGraph_work/ (checkpoints_v3, checkpoints_v4, out_v4, product_assign, validation)
---

# Demand Graph build

> **In one paragraph:** Takes the Amazon US search-term export (200k terms with
> clicked ASINs, categories, and 13-week volume series) and produces an
> immutable, versioned concept graph published to S3 and GitHub, with append-only
> trend observations and a product-assignment layer on top. Runs on a Mac
> (MPS, no CUDA) in under an hour of compute for the core build; the expensive
> parts are the LLM fleets (purification, naming, judging), not the math.

## Inputs

- Amazon export via team S3 (datacore release): 200,000 search terms, each
  with top-clicked ASIN, 1–3 clicked Amazon categories, 56 weekly volume/rank
  points. Trend labels pre-derived upstream (`amazon-search-quantitative-trends`).
- Google-taxonomy crosswalk (99 curated rows) for category anchoring.
- Retailer product package (7,358 products) for the product layer.
- All heavy data lives in `$DEMAND_GRAPH_WORK` (default `~/DemandGraph_work`,
  venv at `venv/bin/python`) — **never in git**.

## Stages

| # | Stage (script) | Input → transformation → output |
|---|---|---|
| 0 | Dedup (`step0`) | 200k raw terms → normalize/accent-fold/token-key merge + ASIN-confirmed typo merges → 170,796 canonicals |
| 1 | Embed (`step1`) | canonicals → BGE-M3 dense CLS, 1024-d, MPS → `embeddings.npy` |
| 2 | Graph (`step2`) | embeddings + clicks → FAISS kNN (k=16, calibrated sim threshold) fused with co-click edges (α 0.7/0.3) → `edges_fused.parquet` (~1.28M edges) |
| 2b | Gate | fused edges → head-noun agreement + modifier-compatibility filter → `edges_gated.parquet` |
| 3 | Cluster (`step7`) | gated graph → Leiden micro (res 1024 tier) → purification removals applied via env → micro niches |
| 3b | Hierarchy (`step3b`) | micro niches → fine-first meta-aggregation (cluster the meta-graph of clusters; singleton-penalty resolution pick) → themes → coarse |
| 4 | Top-level recut (`step8`) | themes → attachment-share gate (≥0.5) keeps real communities; rest fall back to majority Google category → `clusters_v4_1.parquet` + reviewed names CSV |
| 5 | Names/facets (`step4/5`) | clusters → LLM naming fleet + 4-agent name review; brand/IP/audience/language facets → names parquets |
| 6 | Assemble | everything → DuckDB (`demand_graph_v4.duckdb`: concept_terms, trend_observations, nodes, edges, views) + parquets |
| 7 | Product layer (`step9`) | products → embed agent_text → top-5 niche-centroid candidates + head-match flag → candidate-constrained LLM fleet selection → schema-compliant assignments + QA sample |
| 8 | Validate (`validation.py`) | any version → coherence lift, purity, seed stability (sparse ARI), held-out co-click, hierarchy integrity + calibrated judge panel → scorecard; BLOCKED-gate reporting |
| 9 | Publish | artifacts → S3 immutable run + `run_manifest.json` (SHA-256) written **last** → GitHub release |

## Decision points & quality checks

- **Preregister gates before running.** The precision campaign set the 0.70
  pair-precision bar before any experiment; each rung measured by the same
  calibrated panel. No post-hoc goal-moving.
- **Calibrate the measurement instrument first** (see
  [[clustering-methodology-lessons]]): the 3-judge panel was validated on
  hidden known-positives/negatives (100% neg accuracy, 97.5% pos recall)
  before being trusted to grade anything.
- **Acceptance checks before computation:** write the check first; the v1
  overnight run's probe caught a 1-cluster Leiden collapse this way.
- **Resolution selection:** probe a ladder, score with singleton-share
  penalty; never trust a single resolution value across data changes.
- **Sample before full run** — every fleet (purify, naming, product
  assignment) validated on a small chunk before scaling.
- **Immutability rules:** concepts never edited in place, new version = new
  IDs; observations append-only per `observed_period`; S3 runs create-only.

## Outputs & consumers

- Canonical: S3 `processed/showcase/demand-graph/runs/concepts-v4/` (8 objects),
  `.../concepts-v4.1/`, `.../retailer-taxonomy-input/runs/taxonomy_assignment_v41_001/`.
- Team-visible: GitHub release `demand-graph-v4`; PR #18 (codebase); docs in
  repo + Seafile `Archive/Diego/`.
- Local serving: `out_v4/demand_graph_v4.duckdb` (views `cluster_trends`,
  `trending_themes`); explorer HTML.
- Consumers: trend-layer review agent, seasonality branch, buying-list work,
  any retailer-coverage analysis.

## Failure modes & gotchas

- **S3 writes:** plain `aws s3 cp` is DENIED by bucket policy. Only
  `aws s3api put-object --if-none-match '*'` (profile `mantis4retail-s3`)
  works, and only for new keys under `runs/`. Manifest goes last so a partial
  upload is detectable.
- **`tee` swallows exit codes** — run scripts with `set -o pipefail` or a
  FAILed acceptance gate masquerades as exit 0 (this happened; v1).
- **`groupby().indices` on a filtered DataFrame** indexes the *filtered* rows —
  using those indices against a full matrix silently retrieves garbage
  (step9 stage1 bug: "NFL cards" → "armoire", 0.4% head-match; fixed by
  grouping on the full frame → 48.7%).
- **Constraining Leiden inside parent clusters shatters** (144,559 singletons).
  Cluster fine first, aggregate up — never partition down.
- **Model-session usage limits kill agent fleets mid-run.** Chunked fleet
  design with per-chunk files means a killed run loses only unwritten chunks;
  always collect + re-run missing chunks rather than restarting.
- **MPS memory:** BGE-M3 and qwen3-0.6b run comfortably (<4 GB peak, batch
  32); full 170k re-embed ≈ 35 min. `caffeinate` for overnight runs.
- **FlagEmbedding won't import** on the pyenv Python (`_lzma` missing) — load
  BGE-M3 via transformers + `hf_hub_download` of `sparse_linear.pt` directly.
- Another agent may have a branch checked out — do cross-branch work via
  `git worktree`, never by switching the shared working tree.

## Knowledge extracted

- [[demand-graph]] — what the built graph is and its measured quality.
- [[clustering-methodology-lessons]] — which levers moved precision, panel
  calibration, and the v5 bake-off verdict (embedding swap measured MARGINAL,
  not built).
