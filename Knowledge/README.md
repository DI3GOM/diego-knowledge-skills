# Knowledge

Distilled, source-grounded notes produced by the
[`extracting-knowledge`](../skills/extracting-knowledge/SKILL.md) skill,
grouped by theme — one folder per broad area, holding everything about it:

```
Knowledge/
└── <theme-slug>/           # e.g. demand-graph/
    ├── <topic-slug>.md     # topic notes: essentials of a subject
    └── pipeline-<slug>.md  # pipeline notes: registered processes
```

- **Topic notes** — the ~20% of a subject that gives ~80% of the understanding: core concepts, mental models, key facts with sources, pitfalls, open questions.
- **Pipeline notes** — registered information pipelines and processes: inputs, stages, decision points, failure modes, and the knowledge extracted from them.

## Index

<!-- One "### Theme" heading per theme folder; one line per note: - [Name](theme-slug/note.md) — hook -->

### Demand Graph

- [Showcase Demand Graph (concepts-v4.1)](demand-graph/demand-graph.md) — what the 200k-term concept graph is, its measured quality, and how to read its numbers
- [Search-term clustering methodology](demand-graph/clustering-methodology-lessons.md) — which levers actually move cluster precision, LLM-judge calibration, and the v5 bake-off verdict
- [Demand Graph build (pipeline)](demand-graph/pipeline-demand-graph-build.md) — search-term export → versioned concept graph on S3/GitHub, with gates, fleets, and failure modes
