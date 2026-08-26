---
name: extracting-knowledge
description: Capture knowledge into the Knowledge/ folder as structured, source-grounded notes — topic notes distilling the essentials of a subject, and pipeline notes registering important information pipelines or processes (where information comes from, how it flows and is transformed, and the knowledge extracted from it). Use whenever the user wants to learn, research, summarize, or capture the essentials of a subject — "extract the key knowledge about X", "distill this", "add X to my knowledge base" — or wants to document, register, or map a process, workflow, or information/data pipeline — "register this pipeline", "document this process", "capture how this works" — or wants findings from the current conversation preserved, even without the word "knowledge".
---

# Extracting Knowledge

Capture knowledge as compact, source-grounded notes in the knowledge repo. Two note types:

- **Topic note** — distills a subject into the ~20% of ideas that give ~80% of the understanding.
- **Pipeline note** — registers an important information pipeline or process: what feeds it, how information flows and is transformed at each stage, and the knowledge it produces.

Pick by what's being captured: *understanding of a subject* → topic note; *how information moves through a repeatable process* → pipeline note. A pipeline whose output taught you something general may warrant both — the pipeline note links to the topic note.

## Where notes live

Knowledge repo: `/Users/diegomndzuz/Desktop/diego-knowledge-skills/Knowledge/`
- Topic notes: `Knowledge/<topic-slug>.md`
- Pipeline notes: `Knowledge/pipelines/<pipeline-slug>.md`

If that path doesn't exist (different machine), fall back to a `Knowledge/` folder in the current repo; ask only if neither is findable. After writing, add a one-line entry to `Knowledge/README.md`: `- [Name](path.md) — one-line hook`.

## Shared principles

- **Scope first.** Pin down the question behind the request — what should the reader be able to do or decide with this note? Ask one short clarifying question only if the angle is genuinely ambiguous; otherwise state your assumption and proceed.
- **Ground everything.** Every load-bearing fact (numbers, dates, quotes, version-specific claims, stage behaviors) must trace to a listed source. Verify or mark `(unverified)` — never silently include facts you're unsure of.
- **Update, don't duplicate.** Check for an existing note on the subject and extend it instead of creating a near-copy.
- **Absolute dates.** Write "as of 2026-08", never "currently" or "recently".
- **Omit empty sections; target 100–300 lines.** A note that tries to be complete fails at being useful.

## Topic notes

1. **Gather** — model knowledge for the skeleton; web search when the topic is fast-moving or specific facts are load-bearing (prefer primary sources). User-provided sources (files, URLs, this conversation) are primary material — read fully before distilling.
2. **Distill** — for each candidate item ask: *would an expert consider this essential, or merely true?* Keep core concepts, mental models, key facts, pitfalls & misconceptions, open questions. Cut background and anything trivially re-derivable.

```markdown
---
type: topic
topic: <Human-readable name>
date: <YYYY-MM-DD>
angle: <one line — for whom / for what purpose>
sources:
  - <url or file>
---

# <Topic>

> **In one paragraph:** <the whole topic in 3–5 sentences>

## Core concepts
## Mental models
## Key facts
## Pitfalls & misconceptions
## Open questions
```

## Pipeline notes

Registering a pipeline means a reader (or agent) can afterwards understand it, run it, or debug it without re-discovering it. Capture the process *and* what running it has taught you:

1. **Map the flow** — sources/inputs, then each stage as *input → transformation → output*, naming the tools/systems involved. Real observed behavior beats the intended design; if they differ, that difference is a gotcha worth recording.
2. **Capture the judgment** — decision points, quality checks, and failure modes are where the real knowledge lives; a bare step list is re-derivable, the judgment behind it is not.
3. **Extract the knowledge** — what the pipeline's outputs have actually taught you. If that knowledge outgrows the note, move it to a topic note and link it.

```markdown
---
type: pipeline
pipeline: <Human-readable name>
date: <YYYY-MM-DD>
purpose: <one line — what question or decision this pipeline serves>
cadence: <on demand | daily | per release | …>
sources:
  - <url, file, or system>
---

# <Pipeline name>

> **In one paragraph:** what goes in, what comes out, and why it matters.

## Inputs
<where the information comes from — systems, feeds, documents, people>

## Stages
<one subsection or table row per stage: input → transformation (tool) → output>

## Decision points & quality checks
<where judgment is applied; what "good" looks like at each gate>

## Outputs & consumers
<what is produced and who/what uses it>

## Failure modes & gotchas
<how it breaks, how you notice, what to do>

## Knowledge extracted
<key learnings produced by this pipeline so far — or links to topic notes>
```

## Gotchas

- **Conversation capture:** when distilling the current conversation, sources are the artifacts discussed (files, links, tool outputs) — cite those, not "this conversation".
- **Pipelines drift.** When updating a pipeline note after the process changes, note what changed and when — stale stage descriptions are worse than none.
