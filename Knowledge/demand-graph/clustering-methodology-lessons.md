---
type: topic
topic: Search-term clustering methodology — what actually moves quality
date: 2026-08-26
angle: transferable lessons from the demand-graph precision campaign and v5 bake-off, for anyone clustering short queries or judging clusters with LLMs
sources:
  - Mantis4Retail-Repo:Mantis4Retail/analysis/demand-graph/docs/P0_INTERIM_REPORT.md
  - Mantis4Retail-Repo:Mantis4Retail/analysis/demand-graph/docs/DEMANDGRAPH_CLUSTERING_PRODUCTION_REVIEW.md (independent audit)
  - Mantis4Retail-Repo:v5/PREFLIGHT_FINDINGS.md + v5/BAKEOFF_DECISION.md + v5/BAKEOFF_VERIFICATION.md (branch diego/demand-graph-v5-coclick)
  - ~/DemandGraph_work/validation/ (panel_results, confirmation_results per version)
  - /tmp/pair_gold_v4.csv (150-pair judged benchmark)
---

# Search-term clustering methodology — what actually moves quality

> **In one paragraph:** Six versions of the same 170k-term clustering problem,
> each change measured by a calibrated LLM judge panel against preregistered
> gates, produced a clear ranking of levers: structural edge gating and LLM
> purification moved pair precision from 0.32 to 0.687; embedding model swaps
> moved it barely or not at all. The measurement lessons (calibrate the judge,
> use paired statistics, beware scale-confounded metrics, never ship-gate on
> the sample used to select) transfer to any clustering or model-selection
> problem.

## Core concepts

- **Calibrate the instrument before trusting any reading.** The 3-judge LLM
  panel (product-type / shopper / merchandiser lenses, majority vote) was
  validated on hidden known-positive and known-negative pairs: 100% accuracy
  on negatives, 97.5% recall on positives. Only then were its precision
  numbers treated as real. An uncalibrated LLM judge is a random-number
  generator with confidence.
- **Structure beats embeddings for short queries.** The precision ladder:
  better embeddings (e5-small → BGE-M3) ≈ +0.00; finer granularity +0.09;
  **head-noun edge gate +0.17–0.20**; modifier gate confirms ~0.59; **LLM
  purification +0.10** → 0.687±0.074. Two-to-four-word queries carry most of
  their meaning in the head noun; no dense model recovers what a one-line
  grammatical rule enforces.
- **The selection-bias rule:** a benchmark used to *pick* a model cannot also
  *ship-gate* it. The v5 bake-off selected qwen3-0.6b-instruct on the 150-pair
  benchmark; a cutover decision requires ≥200 *fresh* judged pairs, stratified
  to where the measured lift lives.
- **Paired statistics or nothing at small n.** At n=150 pairs, marginal AUC
  CIs span ~0.20 — no achievable improvement clears them. Since every model
  scores the same pairs, the paired bootstrap on the AUC *difference* is the
  valid test (e5's Δ CI [+0.031, +0.119] excludes zero; qwen's touches it).

## Key facts (v5 bake-off, 2026-08-23, independently verified 2026-08-24)

- BGE-M3 dense control 0.596 AUC; qwen3-0.6b-instruct 0.665 (paired Δ +0.070);
  e5-large-instruct 0.670 (Δ +0.074). All short of the 0.70 build bar →
  **MARGINAL, no build**.
- The lift concentrates exactly where the architecture is blind: same-head-noun
  pairs +0.138 AUC, version-numbered products +0.143 (BGE was at coin-flip
  0.500 there — `nba 2k26` vs `wwe 2k26`).
- Known qwen regression: synonym-substitution positives (registration↔document,
  tablet↔kindle). Checked, contained: 8/8 damaged pairs remain co-members of
  the same niche, 5/8 recovered by unconditional co-click edges.
- BGE-M3's sparse/lexical head is **not** a lever: fusion sweep monotonically
  unhelpful on two different dense models (preflight + bake-off).
- Hard negatives mined by different-clicked-ASIN are poisoned:
  P(same-intent | different ASIN) = 0.577 — the "negatives" are half positives.
  Never mine negatives from behavioral non-overlap alone.

## Mental models

- **Raw score gaps across models are meaningless; standardize first.** e5
  compresses all cosines into 0.79–0.98, so its raw pos/neg gap (0.023) looked
  like compression-not-separation. Cohen's d showed all three contenders
  statistically indistinguishable (0.56–0.59) vs BGE's 0.30. Any cross-model
  comparison of raw similarity values is a scale artifact until standardized
  or rank-based. The project hit this twice: the v1 catalog match already had
  to treat e5 similarity scores as rank-only for the same reason.
- **Small embedding models create lexical attractors.** e5-small grouped terms
  on a shared surface word ("Pink items", "Green items") rather than intent.
  Detectable by eye, fixable only partially by bigger models — the durable fix
  was naming them "(lexical)" and excluding them downstream.
- **A failure taxonomy is worth more than the failure rate.** 0.687 precision
  sounds mediocre until you learn all 47 errors were same-theme resolution
  errors, zero cross-category — the graph is never *wrong*, sometimes *coarse*.
  Diagnose before spending on improvement.
- **Measure-first ordering:** when a build is cheap (35 min re-embed) and the
  measurement is expensive (judge fleet), it's tempting to build first. Wrong —
  building first produces a candidate no measurement can gate (selection bias).
  The expensive half decides; run it first.
- **Human agreement is the ceiling.** Published human–human same-intent
  agreement is 60–76%; 0.687 sits inside that band. Chasing 0.75+ pair
  precision may be chasing noise in the definition of "same intent" itself.

## Pitfalls & misconceptions

- "More clusters = better precision" plateaus fast (0.31 → 0.40, then flat).
- Verifying an agent's report means **recomputing its numbers from raw
  artifacts with independent code**, not re-reading its document. The bake-off
  verification reproduced every number but overturned one *argument* (the
  scale-confounded gap comparison).
- LLM naming fleets are reliable but not infallible: a 4-agent review of 376
  names found 33 fixes including one real off-by-one bug (cluster 214). Always
  panel-review names that ship.
- Gated HF models (`google/embeddinggemma-300m`) and pinned remote-code models
  (`gte-multilingual-base` vs transformers 5.15) fail in unattended runs —
  pre-flight model loading before scheduling overnight work.

## Open questions

- Does the qwen lift survive a fresh 200-pair stratified sample (≥80
  same-head, ≥40 version-numbered, ≥30 Spanish, ≥30 synonym-substitution)?
  That single judged sample decides build vs park.
- Spanish-language quality is untested everywhere: only 5/150 benchmark pairs
  touch Spanish.
- Is instruction-prefixing worth 13×? qwen3-plain scored within noise of
  qwen3-instruct (Cohen's d 0.591 vs 0.574) at 4 s vs 53 s embed time.
