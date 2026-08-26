---
name: extracting-knowledge
description: Extract and distill the most important knowledge about a topic into a structured, source-grounded note saved in the Knowledge/ folder. Use whenever the user wants to learn, research, summarize, or capture the essentials of a subject — "extract the key knowledge about X", "distill this", "add X to my knowledge base", "what do I need to know about X" — or wants findings from the current conversation preserved as a knowledge note, even if they don't say "knowledge" explicitly.
---

# Extracting Knowledge

Turn a topic, source, or conversation into a compact knowledge note that captures the ~20% of ideas that give ~80% of the understanding, with every load-bearing fact traceable to a source.

## Workflow

### 1. Scope the topic

Before gathering anything, pin down:
- **The question behind the topic** — what does the user actually want to be able to do or decide with this knowledge?
- **Depth** — orientation overview vs. working knowledge vs. deep reference
- **Angle** — e.g. "Kubernetes" for an app developer is a different note than for a platform engineer

If the topic is broad and the angle is unclear, ask one short clarifying question. Otherwise proceed with a stated assumption.

### 2. Gather

- Start from model knowledge to build the skeleton: core concepts, standard mental models, known trade-offs.
- Use web search when the topic is fast-moving, when specific numbers/dates/versions are load-bearing, or when your knowledge may be stale. Prefer primary sources (official docs, papers, announcements) over blog summaries.
- If the user provided sources (files, URLs, this conversation), those are the primary material — read them fully before distilling.

### 3. Distill

Apply a hard priority filter. For each candidate item ask: *would an expert consider this essential, or merely true?* Keep only:

- **Core concepts** — the handful of ideas everything else hangs on
- **Mental models** — how experts think about the domain (analogies, framings, invariants)
- **Key facts** — numbers, limits, dates, names that change decisions
- **Pitfalls & misconceptions** — what beginners get wrong; counterintuitive truths
- **Open questions** — what is unsettled or worth researching next

Cut background, history, and anything the reader could trivially re-derive. A note that tries to be complete fails at being useful.

### 4. Ground

Every load-bearing fact (numbers, dates, quotes, version-specific claims) must be backed by a listed source. If you can't source it and it matters, either verify it or mark it explicitly as `(unverified)`. Never silently include facts you are unsure of.

### 5. Write the note

Save to the knowledge repo: `/Users/diegomndzuz/Desktop/diego-knowledge-skills/Knowledge/<topic-slug>.md`.
If that path doesn't exist (different machine), fall back to a `Knowledge/` folder in the current repo, and ask only if neither is findable. Use this template:

```markdown
---
topic: <Human-readable topic name>
date: <YYYY-MM-DD>
angle: <one line — for whom / for what purpose>
sources:
  - <url or file — one per line>
---

# <Topic>

> **In one paragraph:** <the whole topic compressed to 3–5 sentences>

## Core concepts
## Mental models
## Key facts
## Pitfalls & misconceptions
## Open questions
```

Omit sections that would be empty rather than padding them. Target 100–300 lines: long enough to be self-sufficient, short enough to be re-read.

### 6. Index

Add or update a one-line entry in `Knowledge/README.md`: `- [Topic](topic-slug.md) — one-line hook`.

## Gotchas

- **Updating beats duplicating.** Before writing, check `Knowledge/` for an existing note on the topic and extend it instead of creating `topic-2.md`.
- **Conversation capture:** when distilling the current conversation, the sources are the artifacts discussed (files, links, tool outputs) — cite those, not "this conversation".
- **Relative dates rot.** Write "as of 2026-08" not "currently" or "recently".
