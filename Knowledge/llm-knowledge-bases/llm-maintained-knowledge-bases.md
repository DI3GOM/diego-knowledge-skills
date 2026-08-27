---
type: topic
topic: LLM-maintained knowledge bases
updated: 2026-08-27
verified: 2026-08-27
angle: design decisions for this repo's Knowledge/ system and extracting-knowledge skill
sources:
  - deep-research agent dossier, 2026-08-27 (URLs inside the raw file)
raw:
  - raw/2026-08-27-kb-research-dossier.md
---

# LLM-maintained knowledge bases

> **In one paragraph:** The dominant pattern (Karpathy's LLM wiki, April 2026) is a three-layer system: immutable raw source snapshots, LLM-compiled notes, and a schema document — with three operations: ingest, query, lint. The load-bearing idea is the grounding invariant: every number, date, and quote in a note must exist verbatim in its linked raw files, which turns truthfulness into a stateless, grep-checkable property. The systems that survive months of use add visible rot (updated/verified dates, Status blocks), triage before writing, and a human promotion gate; the ones that fail drown in confidently-wrong entries, overlong pages, and bland "AI slop" summaries.

## Core concepts

- **Grounding vs attribution.** A listed URL is attribution, not grounding: agent citations resolve (link validity 94%+, relevance 80%+) but factually support the claim only 39-77% of the time (arXiv 2605.06635). Only a frozen local copy makes facts checkable.
- **Compile at ingest, not retrieve at query.** Curated notes read first, sources only for detail; measured 84.6% token savings (47K vs 305K over four same-domain queries, arXiv 2604.11243).
- **Immutability buys stateless verification.** "Because raw/ is immutable, a verified article stays verified" — the whole corpus re-checks in seconds with no incremental state.
- **Bookkeeping is the product.** "the tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping" (Karpathy). Triage dispositions (New/Update/Disputed/No material), append-only logs, and cascade updates are the system.

## Mental models

- **The filename is the retrieval surface.** In a preregistered ablation on a 709-page wiki, "a capable tool-using agent never loads the index, inferring a page's path from the question and reading it directly" (arXiv 2607.04576). Indexes are for humans and preloads; invest in guessable paths.
- **Don't delegate source-weighting to the model.** Models spot fabricated statistics 76-100% of the time in isolation, yet in synthesis impossible statistics received 79% of the credibility boost of valid ones, and models endorsed sources they had themselves flagged 48-96% of the time (arXiv 2606.05403). Independence and authority must be structural fields checked by code.
- **Capture vs promotion.** "Agents can draft freely, but anything that gets promoted to trusted status needs a human review" — the most consistent practitioner prescription.
- **Blandness is low specificity per line.** Chain of Density (arXiv 2309.04269): iteratively fuse in missing salient entities at fixed length. Negative-knowledge slots (pitfalls, open questions) resist generic filler; verbatim-number rules force the specific over the paraphrasable.

## Key facts

- Canonical article size: 80 lines / 715 words (Astro-Han reference implementation); CLAUDE.md files average 287 lines (arXiv 2511.12884). Context rot begins well before window limits; mid-context facts are retrieved worst (Chroma, 18 models).
- Index rot thresholds: fine at 30 pages, manageable at 80, slow past 150 — split per-theme indexes before that.
- Two-date freshness model (OKF extension): `updated` = content changed, `verified` = human confirmed; the gap is the staleness signal. Weekly review, oldest-verified-first.
- Structural supersession: facts sharing a (subject, relation) key with different objects — newer supersedes, older kept and marked (MemStrata, arXiv 2606.26511).
- High-risk claims need two independent sources, independence computed by collapsing duplicate origins/publishers (claude-obsidian, enforced in code).
- Write-time structure pays at read time: A-MEM's seven-field atomic notes hit 45.85 F1 vs MemGPT's 25.52 on temporal reasoning at 2,520 vs 16,977 tokens (arXiv 2502.12110); temporal graphs beat generic memory (Zep 63.8% vs mem0 49.0% on LongMemEval).

## Pitfalls & misconceptions

- **"confidently wrong" is the month-6 failure**: entries the lint pass can't distinguish from good ones — lint checks fidelity to sources, not truth of sources.
- **Maintenance can be a wash**: at 760 pages, "the time I spend maintaining the wiki and the time it saves me are roughly a wash"; worth it mainly for subjects not already well covered on the open web.
- **Pages grow; compaction erodes**: at 1,440+ pages "Pages grow too long and need to be compacted", and repeated LLM self-rewrites flatten detail (model collapse). Split notes; don't re-compress.
- **AI-written summaries read as average**: "it didn't highlight the things I would, and I need to reread anyway" — densification and negative-knowledge slots are the counters, not more prose.
- **The container problem**: theme/topic pages reintroduce classification burden that atomic-note systems dissolve via links; mitigated by broad themes + cascade search, not solved.
- Real upkeep cost even when healthy: 30-45 minutes every 2-3 weeks (contradictions, terminology, stale pages).

## Open questions

- Claim-level quality gates at ingest remain unsolved across all public systems — low-quality sources degrade notes in ways lint can't detect.
- When does this repo need per-theme indexes or hybrid retrieval? (Field ceiling reports: ~150 index entries; ~100 articles / roughly 400,000 words.)
- Would chapter-level ingest granularity (the 155K-word counter-datapoint: 210 concept pages, 4,597 cross-references) beat whole-source raws here?

## See also

- ../agent-skills/ (theme pending — skill-authoring research note)
