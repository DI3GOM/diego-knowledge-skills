# Note templates

Shared frontmatter rules: `updated` = content last changed; `verified` = human last
confirmed (never older than `updated`); `raw:` paths are relative to the note's theme
folder; omit empty sections; ≤120 lines.

## Topic note — `Knowledge/<theme>/<topic-slug>.md`

```markdown
---
type: topic
topic: <Human-readable name>
updated: <YYYY-MM-DD>
verified: <YYYY-MM-DD>
angle: <one line — for whom / for what purpose>
sources:
  - <url or file>
raw:
  - raw/<YYYY-MM-DD-slug>.md
---

# <Topic>

> **In one paragraph:** <the whole topic in 3–5 sentences>

## Core concepts
## Mental models
## Key facts
<every fact carries a number, name, date, or mechanism, located in a raw file first>

## Pitfalls & misconceptions
## Open questions
## See also
<links to related notes — delete links that die; a dead cross-reference is not load-bearing>
```

When a claim is later contradicted or superseded, mark it in place:

```markdown
> **Status: Outdated** (YYYY-MM-DD)
> <what changed and the current understanding, with source attribution>

> **Status: Disputed**
> <each competing claim, each with its own attribution and conditions>
```

## Pipeline note — `Knowledge/<theme>/pipeline-<slug>.md`

```markdown
---
type: pipeline
pipeline: <Human-readable name>
updated: <YYYY-MM-DD>
verified: <YYYY-MM-DD — last date the described process was confirmed to match reality>
purpose: <one line — what question or decision this pipeline serves>
cadence: <on demand | daily | per release | …>
owner: <who or what runs/triggers it>
sources:
  - <url, file, or system>
raw:
  - raw/<YYYY-MM-DD-slug>.md
---

# <Pipeline name>

> **In one paragraph:** what goes in, what comes out, and why it matters.

## Inputs
<where the information comes from — systems, feeds, documents, people>

## Stages
<per stage: input → transformation (tool) → output; link the artifact or source that
evidences each stage — real observed behavior beats intended design, and where they
differ, that difference belongs in gotchas below>

## Decision points & quality checks
<where judgment is applied; what "good" looks like at each gate — the judgment is the
knowledge; a bare step list is re-derivable>

## Outputs & consumers

## Failure modes & gotchas
### Observed
<each with date + evidence — how it broke, how noticed, what was done>
### Hypothesized
<plausible but not yet seen>

## Knowledge extracted
<key learnings this pipeline has produced — link topic notes once a learning outgrows
this section>
```

When the process changes, update the stages, note what changed and when in the body,
and reset `verified` only after re-confirming against the real process.
