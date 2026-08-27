# Knowledge

Distilled, grounded notes produced by the
[`extracting-knowledge`](../skills/extracting-knowledge/SKILL.md) skill,
grouped by theme:

```
Knowledge/
├── log.md                         # append-only ingest log
└── <theme-slug>/                  # e.g. demand-graph/
    ├── raw/YYYY-MM-DD-<slug>.md   # immutable source snapshots (never edited)
    ├── <topic-slug>.md            # topic notes: essentials of a subject
    └── pipeline-<slug>.md         # pipeline notes: registered processes
```

Every number, date, and quote in a note must exist verbatim in its linked `raw/`
files — verify the whole corpus with:

```bash
python3 ../skills/extracting-knowledge/scripts/check_evidence.py .
```

## Index

<!-- One "### Theme" section per theme folder; table: | Note | One-line summary | Updated | -->

### Artemis

| Note | One-line summary | Updated |
|---|---|---|
| [adr-decisions](artemis/adr-decisions.md) | Artemis V1's six binding ADR decisions and the research facts that forced them | 2026-08-26 |
| [registry-ontology-design](artemis/registry-ontology-design.md) | Metadata-registry ontology lessons from five production systems | 2026-08-26 |

### Demand graph

| Note | One-line summary | Updated |
|---|---|---|
| [demand-graph](demand-graph/demand-graph.md) | Showcase Demand Graph (concepts-v4.1): what it is, how good it is, what its numbers mean | 2026-08-26 |
| [clustering-methodology-lessons](demand-graph/clustering-methodology-lessons.md) | Search-term clustering: what actually moves quality | 2026-08-26 |
| [pipeline-demand-graph-build](demand-graph/pipeline-demand-graph-build.md) | Pipeline: raw search-term export → versioned, measured concept graph | 2026-08-26 |

### LLM knowledge bases

| Note | One-line summary | Updated |
|---|---|---|
| [llm-maintained-knowledge-bases](llm-knowledge-bases/llm-maintained-knowledge-bases.md) | How LLM-maintained knowledge bases succeed (grounding invariant) and fail (confidently-wrong rot) | 2026-08-27 |
