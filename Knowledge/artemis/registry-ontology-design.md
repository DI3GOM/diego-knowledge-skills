---
type: topic
topic: Metadata-registry ontology design — lessons from five production systems
date: 2026-08-26
angle: for designing any dataset/artifact registry — why the entity set converges, where abstraction helps vs corrupts, and where OWL/catalogs actually belong (distilled from the Artemis ADR-002 research and the Alexios review exchange, 2026-08-18)
sources:
  - /Users/diegomndzuz/Desktop/ArtemisDocs/adrs/002-postgres-registry.md (esp. D4/D4b + alternatives)
  - Marquez Postgres schema (74 Flyway migrations), OpenLineage spec 2-0-2
  - google/ml-metadata proto + DDL (v1.21.0)
  - DataHub v1.7.0 metamodel; OpenMetadata 1.13.3 DDL
  - dagster 1.13.18 storage schemas
  - https://en.wikipedia.org/wiki/Command_Query_Responsibility_Segregation
---

# Metadata-registry ontology design

> **In one paragraph:** Every mature metadata system — Marquez/OpenLineage, ML-Metadata, DataHub, OpenMetadata, Dagster — independently converges on the same five concepts: *thing, version-of-thing, execution, edge, check-result*. A registry ontology should therefore be stolen, not invented, and kept small, typed, and closed-world. The two seductive generalizations both fail in documented ways: "one maximally-abstract entity" (EAV) destroyed ML-Metadata's queryability until it deleted its own query language, and "ontology as OWL + reasoner" runs on open-world logic that cannot even express "this version is missing its checksum" as a violation. The resolution is a two-ontology split: the registry's own schema is fixed and relational; the *domain ontologies of ingested corpora* are data the registry stores — and that's where auto-generation, URIs, and reasoners legitimately live.

## Core concepts

- **The convergent five.** Dataset / DatasetVersion / Run–Execution / lineage Edge / Assertion-result appear under different names in all five systems surveyed. When independent teams converge, the entity set is not a design risk — the abstraction ceiling is already known.
- **Immutable version rows + mutable head pointer + aliases.** MLflow deprecated its one-of-N *stages* in favor of *aliases* precisely because "promotion is an alias reassignment, not a state transition"; DataHub and Marquez use the same shape (`current_version` pointer, `isLatest` maintained flag, separate sortable `sort_id`).
- **Typed properties + free `custom_properties`.** MLMD's best idea: declared, typed fields per entity type *plus* one free-form bag. In Postgres: real columns + one JSONB, with hot JSONB fields promoted as `GENERATED ALWAYS AS (...) STORED` columns (OpenMetadata's pattern — constraints without dual-write).
- **Two-ontology split (Artemis ADR-002 D4b).** Registry ontology: small, fixed, closed-world, relational — the schema the system *runs on*. Domain ontologies of ingested corpora: per-client, discovered, possibly auto-generated OWL/RDF with URIs — *data the system stores*. Collapsing them is the inner-platform effect: a registry whose schema is "anything" can guarantee nothing about itself.

## Mental models

- **"Abstract where it's free, concrete where constraints and queries live."** The generic layer (JSONB bag) costs nothing until a field is used to filter, sort, join, or constrain — then it gets promoted to a typed column. Promotion via generated columns is an `ADD COLUMN`, no backfill, no drift.
- **Reasoner consistency ≠ data correctness.** OWL reasoning checks class-level coherence under the open-world assumption (absence ≠ falsity, no unique names). Registry integrity is the opposite regime: closed-world, "absence is a violation" — natively what FK/CHECK/NOT NULL do; rebuilding it in RDF means bolting SHACL onto a triple store to reimplement Postgres.
- **Catalogs are consumers, not registries.** OpenMetadata/DataHub/Unity Catalog are discovery-and-governance layers that *ingest from* systems of record. They have no home for transactional concerns (processing requests, idempotency keys, artifact state machines, head pointers). Emit a standard (OpenLineage) and any catalog can be added downstream later, unchanged registry.
- **Macro-CQRS beats in-app CQRS for data platforms.** Commands = processing requests → orchestrator runs; queries = registry reads + a physically separate read model (versioned manifests/Parquet in the lake); append-only `run_states`/`lineage_events` are the event log. The CQRS benefits arrive at the architecture level without in-process buses — Fowler's caution about CQRS-as-code applies.

## Key facts

- **MLMD is the EAV cautionary tale** (as of 2026-08): pure EAV property storage (six typed value columns, NULL-heavy, zero foreign keys) made filtering so hard the project embedded a full query language (ZetaSQL `filter_query`) — then **deleted it in v1.21.0** as unmaintainable. The project is feature-frozen; Kubeflow is actively removing it.
- **JSONB has no planner statistics** — Postgres defaults to a hardcoded ~0.1% selectivity; a documented case ran 584 s vs 300 ms (~2000×) off a 124,616× row misestimate. This is the *efficiency* answer to "why not one abstract blob": not disk, but plans.
- **OpenMetadata's frozen-ordinal enum** (`relation SMALLINT` indexing an append-only enum, complete with an unfixable typo) and its **float version numbers** (`multipleOf: 0.1`) are the two documented anti-patterns to never copy; store enum strings/`TEXT+CHECK`, use two integer version columns.
- **Marquez's scar tissue, free to inherit:** shred facets from day one (their V55 backfill needed a migration lock table); `TIMESTAMPTZ` from day one (V73 converted every column); `dataset_symlinks` exists because names aren't stable across producers — plan it early.
- **Dagster's check-results carry a pointer to the exact materialization evaluated** and split stored-status from *resolved*-status (reconciled against run state, so dead runs surface as `EXECUTION_FAILED`, not zombie `PENDING`) — both patterns belong in any validation-findings table.
- Identity consensus: surrogate PK (UUIDv7) + natural key `UNIQUE(namespace, name)` + `external_id` for reconciliation; content hashes as separate UNIQUE columns, never as PKs.

## Pitfalls & misconceptions

- *"Define one very abstract thing and go from there"* — the failure isn't runtime cost at small scale; it's integrity (no per-attribute constraints), plans (no stats), migrations-as-app-code, and a schema that stops documenting the domain. The workable 80% of the idea is the typed-properties + JSONB + promotion pattern.
- *"Auto-generate the ontology, URIs everywhere, verify with reasoners"* — right instinct, wrong layer: it belongs to the corpus-understanding side (per-client domain ontologies as stored artifacts), not the registry schema. URIs are already free (`(namespace,name)` + OpenLineage naming); RDF/DCAT/PROV-O output is an emission projection, not a storage decision.
- *"OpenMetadata is too OP — just adopt it"* — capability real, fit wrong: it's a governance layer plus a Java server + search index + own DB (≈ the whole platform's footprint again at team size 3–5). Steal its schema ideas; optionally deploy it later as an OpenLineage consumer for the catalog UI.
- *"Store OpenLineage events as the registry"* — OL's core model has no run state or timestamps outside facets, and even funded vendor consumers implement the spec partially. Emit OL; don't *be* OL.

## Open questions

- Whether the Bacchus/knowledge-graph layer's auto-generated corpus ontologies should standardize on OWL+SHACL or stay property-graph-shaped — deferred until that layer is designed (the registry stores either as artifacts).
- OpenMetadata 2.0's entity-versioning changes were still RC as of 2026-08 — re-check before copying anything from that mechanism.
