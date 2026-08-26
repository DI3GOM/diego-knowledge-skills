# Knowledge

Distilled, source-grounded notes produced by the
[`extracting-knowledge`](../skills/extracting-knowledge/SKILL.md) skill.

Two note types:
- **Topic notes** (`<topic-slug>.md`, in this folder) — the ~20% of a subject that gives ~80% of the understanding: core concepts, mental models, key facts with sources, pitfalls, open questions.
- **Pipeline notes** ([`pipelines/`](pipelines/)) — registered information pipelines and processes: inputs, stages, decision points, failure modes, and the knowledge extracted from them.

## Index

<!-- One line per note: - [Name](path.md) — one-line hook -->

### Topics

- [Showcase Demand Graph (concepts-v4.1)](demand-graph.md) — what the 200k-term concept graph is, its measured quality, and how to read its numbers
- [Search-term clustering methodology](clustering-methodology-lessons.md) — which levers actually move cluster precision, LLM-judge calibration, and the v5 bake-off verdict

### Pipelines

- [Demand Graph build](pipelines/demand-graph-build.md) — search-term export → versioned concept graph on S3/GitHub, with gates, fleets, and failure modes
