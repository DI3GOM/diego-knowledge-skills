---
name: extracting-knowledge
description: Capture knowledge into the Knowledge/ folder as structured, source-grounded notes — topic notes distilling the essentials of a subject, and pipeline notes registering important information pipelines or processes (where information comes from, how it flows and is transformed, and the knowledge extracted from it). Use whenever the user wants to learn, research, summarize, or capture the essentials of a subject — "extract the key knowledge about X", "distill this", "add X to my knowledge base" — or wants to document, register, or map a process, workflow, or information/data pipeline — "register this pipeline", "document this process", "capture how this works" — or wants findings from the current conversation preserved, even without the word "knowledge".
---

# Extracting Knowledge

Capture knowledge as compact, grounded notes in the knowledge repo. Two note types:

- **Topic note** — distills a subject into the ~20% of ideas that give ~80% of the understanding.
- **Pipeline note** — registers an information pipeline or process: what feeds it, how information flows and transforms per stage, and the knowledge it produces.

Pick by what's captured: *understanding of a subject* → topic; *how information moves through a repeatable process* → pipeline. Templates for both are in `references/templates.md` — read it before writing a note.

## Repo layout

Knowledge repo: `/Users/diegomndzuz/Desktop/diego-knowledge-skills/Knowledge/` (fallback: a `Knowledge/` folder in the current repo; ask only if neither is findable).

```
Knowledge/
├── README.md                      # human-facing index: one table per theme
├── log.md                         # append-only ingest log
└── <theme-slug>/                  # one folder per broad area, e.g. demand-graph/
    ├── raw/YYYY-MM-DD-<slug>.md   # IMMUTABLE source snapshots — never edit or delete
    ├── <topic-slug>.md            # topic notes
    └── pipeline-<slug>.md         # pipeline notes
```

Themes are broad ("demand-graph", "llm-tooling") — reuse an existing theme folder before creating one; a theme that would hold a single note forever is too narrow. **Name notes so the path is guessable from a question about them** — agents retrieve by inferring paths and grepping, not by reading the index; the filename is the retrieval surface.

## The grounding invariant

Every load-bearing fact in a note — numbers, dates, direct quotes — must exist **verbatim** in the `raw/` files that note links. This makes truthfulness a grep-checkable property instead of a hope:

- **Snapshot sources first.** Before writing a note, save each substantive source (fetched page content, report, transcript, key excerpts of a conversation) as `raw/YYYY-MM-DD-<slug>.md`. Raw files are immutable — a verified note stays verified. A URL alone is attribution, not grounding: pages change, and a link says nothing about whether the fact is really there.
- **Locate before you write.** Find each value in the raw file before writing it, and write it exactly as found — if the source says 42K, write 42K, not 42,000. Derived values (sums, deltas) must show their components. Can't locate it? Drop it, state it without precision, or mark it `(unverified)`.
- **Lint:** run `scripts/check_evidence.py <Knowledge-dir>` to verify the whole corpus — it greps each note's high-signal literals (quotes, dates, specific numbers) into its linked raws and reports misses. Report-only: never auto-fix facts.

## Workflow

1. **Triage.** Search existing notes (and `log.md`) for the subject's key entities and synonyms, then decide: **New** note / **Update** existing / **Disputed** (conflicts with existing — see below) / **No material** (adds nothing beyond what's already held: keep the raw, log it, stop — never force a note out of a thin source).
2. **Gather.** Model knowledge for the skeleton; web search when facts are load-bearing or fast-moving; prefer primary sources. For any claim you expect to conclude, **deliberately search the opposing side** — failures, criticism, contradicting reports.
3. **Distill.** Keep only what an expert would call essential, not merely true. Then run a densification pass: list salient entities/numbers present in the sources but missing from the draft, and fuse them in *without growing the note* — blandness is low specificity per line. Every key fact needs a number, name, date, or mechanism.
4. **Write** using the template. ≤120 lines; the first line after the title is a one-paragraph summary. Split on overflow rather than compressing — repeated self-compression flattens detail.
5. **Log & index.** Append to `log.md`: `## [YYYY-MM-DD] ingest | <title> — Disposition: New|Update|Disputed|No material`, with raw path and any other notes updated. Update the theme's table in `README.md` (`| Note | One-line summary | Updated |`).
6. **Cascade.** Don't stop at the index — grep the whole `Knowledge/` tree for the source's key entities and update every note the new information materially affects.

## Keeping notes truthful over time

- Frontmatter carries two dates: `updated` (content last changed) and `verified` (human last confirmed accuracy). `verified` never predates `updated`; the gap between them is the staleness signal.
- **Never silently rewrite history.** When new information contradicts a note, keep the old claim and mark it with a dated `> **Status: Outdated**` block saying what changed, per the template. Competing live claims get `> **Status: Disputed**` with each position attributed.
- **Conflicting sources: never average.** State that sources disagree and why, then give each position its own lines with its conditions. A blended midpoint is a fabricated number.
- Absolute dates always ("as of 2026-08", never "currently").

## Gotchas

- **Conversation capture:** sources are the artifacts discussed (files, links, tool outputs) — snapshot those into `raw/`, don't cite "this conversation".
- **Pipeline notes must separate observed from hypothesized** — a failure mode with a date and evidence is knowledge; one you imagined is a guess. The template enforces this.
- **Moving a note between themes** is fine — move the file, fix the index and inbound links.
