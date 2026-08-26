---
type: topic
topic: Showcase Demand Graph (concepts-v4.1)
date: 2026-08-26
angle: for anyone consuming or extending the Mantis4Retail demand graph — what it is, how good it is, and what its numbers mean
sources:
  - Mantis4Retail-Repo:Mantis4Retail/analysis/demand-graph/docs/PROJECT_CHRONICLE.md (branch diego/demand-graph-explorer)
  - Mantis4Retail-Repo:Mantis4Retail/analysis/demand-graph/docs/P0_INTERIM_REPORT.md
  - Mantis4Retail-Repo:Mantis4Retail/analysis/demand-graph/docs/V4_1_BRIEF.md
  - s3://mantis4retail-proto-428156589460-us-east-1/processed/showcase/demand-graph/runs/concepts-v4.1/
  - ~/DemandGraph_work/validation/ (per-version scorecards + panel results)
  - GitHub release demand-graph-v4 (Mantis4Real/Mantis4Retail-Repo)
  - Seafile Archive/Diego/Demand_Graph_Build_2026-08-19/ (v1 deliverables + README with known limitations)
---

# Showcase Demand Graph (concepts-v4.1)

> **In one paragraph:** A knowledge graph over the 200,000 Amazon US search
> terms in the Showcase export, deduplicated to 170,796 canonical terms and
> clustered into a 3-level demand hierarchy (8,873 micro niches → 2,513 themes
> → 226 named communities + 19 category fallbacks). Concepts are immutable and
> versioned; trends and products attach as separate, replaceable layers. Every
> quality claim is measured by a calibrated 3-judge LLM panel, not assumed.
> Built 2026-08-17 → 2026-08-20; v4.1 is the serving version as of 2026-08.

## Core concepts

- **Concept/observation split.** The clustering ("concepts") is immutable and
  versioned (`concepts-v4.1`); trend data lives in append-only
  `trend_observations` keyed by `observed_period` + `method_version`. Products
  attach by assignment runs. This lets trends and catalogs change without ever
  rebuilding or invalidating the graph.
- **Three-level hierarchy, 100% strictly nested:** micro niche (tight
  same-product-type groups, avg ~19 terms) → theme → top level. The top level
  (v4.1) only keeps a graph community as parent where a theme's external edge
  weight genuinely points into it (attachment share ≥ 0.5); the other ~90% of
  themes fall back to their majority Google category. Honesty over prettiness.
- **Evidence fusion:** semantic kNN (BGE-M3 dense embeddings, FAISS, k=16)
  fused with behavioral co-click edges (shared top-clicked ASIN). Nominal
  weights 70/30 but **effective evidence is 94.6/5.4** by weight — the graph is
  mostly semantic; co-click is a thin, high-precision correction.
- **Edge gating is the precision lever.** Head-noun agreement + modifier
  compatibility gates on edges (from the KG research brief) moved pair
  precision more than any embedding change: 0.40 → 0.57–0.60.
- **LLM purification:** a 20-agent fleet reviewed all 11,818 micro niches and
  expelled 12,712 misfit terms (versioned removals artifact) → final precision
  0.687 ± 0.074.
- **Soft membership:** 36% of terms genuinely belong to multiple contexts;
  weighted multi-cluster membership derived from fused edge weights. Broad
  terms spread over their specializations — is-a structure emerges as weights.

## Key facts

- Dedup: 200,000 → 170,796 canonicals; 9,056 typo merges confirmed by shared
  clicked ASIN.
- Pair precision ladder (calibrated panel, preregistered 0.70 gate):
  v1 0.32 → BGE-M3 0.31 → finer granularity 0.40 → head-gate 0.57–0.60 →
  modifier gate 0.587 (n=150 confirm) → **purification 0.687 ± 0.074** =
  gate met within 95% CI. For context, published human–human agreement on
  same-intent judgments is 60–76%.
- Fine-level volume-weighted category purity **0.956**; coherence lift 6.8×;
  top-level purity 0.742 (v4 forced adoption) → **0.819** (v4.1 recut).
- Hierarchy: nesting 11.8% (v1) → **100%** (fine-first meta-aggregation);
  coarse ARI 0.61 → 0.887.
- Failure taxonomy: all 47 judged-"no" pairs in the confirm sample were
  *same-theme resolution errors* (too-coarse niche), zero cross-category
  membership errors. Residual error is granularity, not wrongness.
- Trend layer: 13 weekly points per term (`sv1..sv8` recent + `sv52..sv56`
  same weeks prior year). One observed period exists (`2026-08-05`) — drift,
  churn, velocity, and any forward-scoring are **unmeasurable until a second
  release lands**. Trend labels are descriptive, never validated predictive.
- Facets: 2,389 Spanish-driven terms flagged at v1; brand / IP / audience /
  language facets carried on every term since.
- Product layer lineage: v1 matched 13,209 products (1,626 Showcase + 11,583
  TikTok Shop) to fine-cluster centroids with a head-noun acceptance gate —
  68% accepted (9,023). Superseded by the v4.1 assignment below.
- Product layer: 7,358 products (Showcase US/CA, MINISO, Five Below) assigned
  to micro niches — 95.2% assigned, QA precision **0.953 ± 0.034**.
  Cross-retailer signal: Showcase-only niches include squishies (97 products)
  and Labubu (59); competitor-only include graphic tees (69), iPhone cases (43);
  242 niches contested.
- Where it lives: S3 runs `processed/showcase/demand-graph/runs/concepts-v4/`
  and `.../concepts-v4.1/` (canonical, immutable); GitHub release
  `demand-graph-v4`; local serving DB
  `~/DemandGraph_work/out_v4/demand_graph_v4.duckdb`.

## Mental models

- **The graph is a stable coordinate system; everything else is weather.**
  Niches are the coordinates; trends, products, and coverage are observations
  plotted onto them. Never bend the coordinates to fit one week's weather.
- **Precision and purity answer different questions.** Purity 0.956 says
  "niches don't mix categories"; pair precision 0.687 says "two random terms
  in a niche mean the same thing." A niche can be 100% pure and still too
  coarse. Quote the right number for the claim being made.
- **Junk is caught, not hidden:** junk-catcher and lexical clusters (names
  containing "Ambiguous", "lexical", "titles", "mixed") exist by design and
  must be excluded from any client-facing ranking.

## Pitfalls & misconceptions

- **Don't read v4.1's top-trending list as insight** — built in August it
  re-detects back-to-school (v1's raw radar top was literally JanSport
  backpacks, 81% trending). Use `deseasonalized_trending` — defined as
  trending AND >50% of the cluster's terms above their last-year same-period
  baseline — but know it is label-based, not a baseline model.
- **Micro-niche IDs are not stable across versions** (seed stability is
  inherently low at that granularity). Council ruling from v1 stands: cluster
  IDs are internal and disposable — month-over-month reporting keys on
  taxonomy categories, brands, and IPs, which are stable. Serve micro niches
  via their theme + lineage, never by bare ID comparison across versions.
- **Lexical-attractor clusters** ("Pink items", "Green items"): embeddings can
  group on a shared surface word (a color) rather than intent — endemic with
  the small v1 model, reduced but not eliminated by BGE-M3 + gating. They are
  marked "(lexical)" in names precisely so they can be filtered.
- **12,712 expelled terms and 353 unassigned products exist.** Any coverage
  claim ("every term sits in a niche") must footnote them.
- **The held-out co-click metric is structurally unfair to gated graphs** —
  gating deliberately removes recoverable-but-wrong edges. Don't compare gated
  vs ungated versions on it.

## Open questions

- Forward test: freeze self-scores now, score against the next Amazon data
  release (snapshot frozen; release not arrived as of 2026-08-26).
- Sales backtest permanently blocked: client cannot supply sales data.
- v5 embedding upgrade: measured but not built — see
  [[clustering-methodology-lessons]] for the bake-off verdict.
- The three buying lists (niche coverage × trends join) remain unbuilt — the
  step that turns the graph into purchasing decisions.
