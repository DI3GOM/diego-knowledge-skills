# Raw: LLM-maintained knowledge bases — research dossier excerpts

Source: deep-research agent report, collected 2026-08-27 (web research sweep dated
2026-08-26/27). Verbatim excerpts of the load-bearing claims, with the URLs the
dossier cites.

## Karpathy LLM wiki lineage
- Karpathy gist (April 2026): "the tedious part of maintaining a knowledge base is
  not the reading or the thinking — it's the bookkeeping."
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Reference implementation Astro-Han/karpathy-llm-wiki. Grounding invariant:
  "Every load-bearing fact in wiki/ — numbers, dates, direct quotes — exists
  verbatim in the raw/ files linked by that article's Raw field." "Because raw/ is
  immutable, a verified article stays verified."
- Source-fidelity rule: "if the source says 42K, write 42K, not 42,000."
- check_evidence.py candidate set: quotes of 15+ characters; ISO dates; numbers
  thousands-grouped, dotted, suffixed (42K, 99.9%), or 4+ digits. Report-only:
  "Report findings; never auto-fix facts."
- Production baseline: 94 wiki articles / 13 topic directories / 99 raw sources /
  87 log entries in 7 days. Shipped example article: 80 lines / 715 words.
- Triage dispositions: New / Update / Disputed / No material. "Do not force an
  article out of a thin source."
- "Never silently rewrite history." Status blocks: Outdated (dated) / Disputed.
- Cascade rule: "Do not rely on the index alone: search the full wiki for the
  source's key entities, aliases, and the claims it touches."
- Adversarial research rule: "deliberately search the opposing side: failures,
  criticism, failed replications."

## Empirical results
- Progressive-disclosure preregistered ablation, arXiv 2607.04576, real 709-page
  LLM-maintained wiki: "a capable tool-using agent never loads the index,
  inferring a page's path from the question and reading it directly." Cost falls
  "from about a third for a self-routing agent to well over half under
  catalog-preload"; quality non-inferior.
- Cited but Not Verified, arXiv 2605.06635 (14 models, 130 queries): link
  validity 94%+, topical relevance 80%+, factual support only 39-77%. Grounding
  degrades ~42% as tool-call depth grows from 2 to 150.
- Trust, but Don't Verify, arXiv 2606.05403: models identify fabricated
  statistics 76-100% of the time in isolation, but in multi-source synthesis
  structurally impossible statistics received 79% of the credibility boost that
  valid ones did; models flagged fabrications in their own reasoning traces yet
  still endorsed those sources 48-96% of the time.
- Knowledge compounding, arXiv 2604.11243: compile-at-ingest used 47K vs 305K
  tokens over four same-domain queries — 84.6% savings; 30-day projections 53.7%
  (medium) and 81.3% (high topic concentration).
- A-MEM, arXiv 2502.12110: seven-field atomic notes + memory evolution; LoCoMo
  temporal reasoning 45.85 F1 vs MemGPT 25.52; 2,520 vs 16,977 tokens (85%
  reduction).
- Zep/Graphiti temporal knowledge graph: 63.8% vs mem0 49.0% on LongMemEval.
- Context rot (Chroma, 18 frontier models): every model degrades as input grows,
  beginning well before the window limit; mid-context facts retrieved worst.
  https://www.trychroma.com/research/context-rot
- Agent READMEs, arXiv 2511.12884: CLAUDE.md mean 287 lines (SD 112); AGENTS.md
  mean 142 lines (SD 231).
- Chain of Density, arXiv 2309.04269 (ACL NewSumm 2023): iteratively identify
  missing salient entities and fuse them in at fixed length; humans preferred CoD
  summaries over vanilla-prompt summaries.
- MemStrata, arXiv 2606.26511: "if an incoming fact and a stored fact share a
  (subject, relation) key but assert different objects, the newer one supersedes
  the older."

## Freshness and provenance models
- Google Open Knowledge Format OKF v0.1, released 2026-06-12, ships only an
  `updated` timestamp. Curtner extension: `updated` = content last changed,
  `verified` = when a human last confirmed accuracy; the failure it solves —
  "had lost the ability to distinguish between 'verified current' and 'untouched
  for eight months.'" Weekly review, oldest-verified-first; dispositions
  confirm / correct / defer with target date / archive.
  https://www.scottcurtner.com/articles/okf-freshness/
- claude-obsidian ledgers: authorities {official, primary, secondary, community,
  synthetic, unknown}; assessments {accepted, provisional, contested,
  unsupported, deprecated}; hard rule enforced in code: "high-risk acceptance
  requires two independent sources", independence computed structurally by
  collapsing duplicate origins/publishers. "Never fabricate evidence locators,
  quotations, page numbers, or confidence."
  https://github.com/AgriciDaniel/claude-obsidian

## Practitioner failure reports
- HN: "Six months in, you have entries that are confidently wrong and the lint
  pass can't tell which." https://news.ycombinator.com/item?id=47899844
- One-month field report at 760 pages (430 human-reviewed): "the time I spend
  maintaining the wiki and the time it saves me are roughly a wash"; "the wiki
  doesn't update itself by default."
  https://www.rdworldonline.com/is-karpathys-viral-llm-wiki-helpful-mostly-yes-one-month-in/
- Index rot thresholds (field-measured): fine at 30 pages, manageable at 80,
  "past 150 pages, scanning the full index on every query becomes slow."
  https://mono.hr/2026/04/22/LLM-Wiki-Personal-Knowledge-Management/
- Casey Newton at 1,440+ pages: "Pages grow too long and need to be compacted";
  rewrote the system away from "Claude's hyper-compressed, borderline-unreadable
  house style." https://www.platformer.news/karpathy-llm-wiki-journalism-productivity/
- 25,979-file vault owner: "my own, much more valuable thoughts get diminished by
  'AI Slop'"; on-the-spot summaries "very average... it didn't highlight the
  things I would, and I need to reread anyway."
  https://www.ssp.sh/brain/using-obsidian-with-ai/
- HN consensus fix: "separate the capture layer from the promotion layer. Agents
  can draft freely, but anything that gets promoted to trusted status needs a
  human review."
- Zettelkasten critique of topic pages — the container problem: topic aggregation
  reintroduces the classification problem; "One card, one concept. Links replace
  classification." https://yu-wenhao.com/en/blog/karpathy-zettelkasten-comparison/
- Reported real maintenance cadence: 30-45 minutes every 2-3 weeks on
  contradiction checks, terminology normalization, stale-page cleanup.
- Verdent guide: wiki pattern's ceiling "around 100 articles and roughly 400,000
  words" before hybrid retrieval is needed.
  https://www.verdent.ai/guides/llm-knowledge-base-coding-agents
- Counter-datapoint (HN, 155K words / 68 source files): chapter-level ingest
  granularity produced 210 concept pages with 4,597 cross-references and surfaced
  genuine cross-source contradictions unprompted.
