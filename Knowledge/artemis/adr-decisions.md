---
type: topic
topic: Artemis V1 — the ADR decision set
date: 2026-08-26
angle: for anyone implementing or reviewing Artemis V1 — the six binding decisions and the research facts that forced them
sources:
  - /Users/diegomndzuz/Desktop/ArtemisDocs/adrs/ (ADR-001…006, drafted 2026-08-17)
  - /Users/diegomndzuz/Desktop/ArtemisDocs/v1-artemis-proposal-merged.md
  - https://github.com/apache/iceberg-python (issues #1551, #2604, #3319, #3758)
  - https://github.com/duckdb/duckdb-iceberg/issues/805
  - https://github.com/dagster-io/dagster/issues/33439
  - https://dagster.io/prefect (acquisition FAQ)
  - AWS Price List API us-east-1 (effective 2026-08-01); AWS Security Hub FSBP controls
---

# Artemis V1 — the ADR decision set

> **In one paragraph:** Artemis (the data layer under Mantis) was specified in six ADRs on 2026-08-17, each backed by primary-source research. The spine: Iceberg **format v2** on plain S3 with the Glue catalog spoken to via its **Iceberg REST endpoint**; an **RDS Postgres 17** registry whose ontology is stolen from five production metadata systems; a FastAPI service with lax-FCIS layering and a committed OpenAPI snapshot as the contract; **Terraform** with S3-native state locking and OIDC; FSBP-anchored per-service AWS standards with documented suppressions; and **Dagster OSS on ECS Fargate** with specific defect patches. V1 never touches Mantis — Artemis pushes into Mantis's existing developer API. Total steady-state infra ≈ $100–150/mo.

## Core decisions (one line each, with the forcing fact)

| ADR | Decision | The fact that forced it |
|---|---|---|
| 001 | Pin Iceberg **format-version 2** explicitly | PyIceberg cannot write v3 (`NotImplementedError` in source); Athena cannot read v3 (pinned to Iceberg 1.4.2); v3 is a one-way door |
| 001 | Glue catalog **via REST endpoint**, not `type: glue` | REST makes any future catalog (S3 Tables, Polaris, Unity) a URI change; costs nothing |
| 001 | **No partitioning; one table per (dataset, version)** | AWS floor: a partition should hold 2–5× target file size (≈256–640 MB); whole Artemis tables are 25–150 MB. Tags can't be addressed by name in Athena or DuckDB |
| 002 | **RDS PG 17 `db.t4g.small`** (~$26/mo), not Aurora | Aurora's smallest PG instance is `db.t4g.medium` (~2×); ASv2 never pauses under an always-on API and silently skips scheduled jobs while paused |
| 002 | Two logical DBs (`artemis_registry` + `dagster`), one instance | Dagster has no schema-isolation option (closed as not-planned); DB-level is the supported boundary and blinds Alembic autogenerate to Dagster's tables |
| 003 | Commit in the **service layer**, never in a `yield` dependency | FastAPI ≥0.118 runs dependency exit *after* the response — a failed commit returns a 200 |
| 003 | Contract = committed `openapi.json` + oasdiff + Schemathesis; no Pact | Dredd and Optic are both archived; Pact pays only when the consumer team runs it too |
| 004 | **Terraform**, OpenTofu as named contingency; S3-native state locking | CDKTF archived 2025-12-10 (no hybrid path); HCP free tier ended 2026-03; DynamoDB locking deprecated by HashiCorp and AWS |
| 004 | One member account, plain Organizations, **no Control Tower** | Control Tower's Config recording bills per resource daily — worst case under per-run Fargate task churn |
| 006 | Dagster OSS on ECS: daemon singleton, `QueuedRunCoordinator`, `S3ComputeLogManager` | >1 daemon unsupported; default coordinator makes UI-runs and scheduled runs inherit *different* configs; default compute logs vanish with the Fargate filesystem |

## Mental models

- **Decide on operational grounds when cost collapses.** The entire Iceberg catalog+storage+maintenance spread at 500 GB is ~$12–25/mo — cost is deliberately *not* an input to that decision.
- **Documented suppression over silent skip.** Three Security Hub controls are structurally wrong for Artemis (S3.17 on analytics buckets, CloudWatch.16's 365-day retention floor vs 30-day app logs, ECS.5 vs debug Exec); each gets a written suppression, never a quiet failure.
- **Revisit triggers, not permanent truths.** Every ADR ends with the observable condition that reopens it (e.g., v3 becomes usable when *both* PyIceberg writes it *and* Athena reads it).
- **The registry is the durable side; Dagster's DB is prunable operational state.** Never SQL into Dagster's serdes-encoded blobs; bridge via recorded `run_id`/`asset_key`/`storage_id`, pushed from inside pipelines.

## Key facts (load-bearing, verified 2026-08)

- **PyIceberg pin: `0.11.1` exactly.** No built-in commit retry (retry lands in 0.12.0 via #3319) → a retry wrapper is mandatory own-code; 0.12.0rc1 was pulled from PyPI over a silent upsert corruption on temporally-partitioned tables (#3758, fix unmerged as of 2026-08-17).
- **PyIceberg `expire_snapshots()` is metadata-only** — zero storage I/O; it strands orphans PyIceberg cannot delete. File reclamation = Glue table optimizers (verified to work on PyIceberg-written tables) or Athena `VACUUM` (silently no-ops without `s3:DeleteObject`).
- **Athena `OPTIMIZE` silently truncates µs timestamps to ms** (PyIceberg writes µs) — banned. Whether Glue managed compaction shares the flaw is undocumented → open spike.
- **Manifest compaction has no managed AWS answer** — only Trino's `optimize_manifests`. Table-per-version layout keeps manifests trivial; standing append tables are the watch case.
- **Prefect acquired Dagster Labs** (announced 2026-07-13, closed Aug 2026). License verified still Apache-2.0, releases on cadence; quarterly check written into ADR-006. Choosing Prefect no longer hedges Dagster risk — same owner.
- **Dagster open bugs shaping config:** #33439 (ECS `RunTask` "Rate exceeded" throttling not retried — mitigate with `max_concurrent_runs`); Postgres pool size not tunable (size RDS `max_connections` against peak run tasks, not the 3 services); official ECS Terraform module has 3 defects (plaintext DB password, `s3:*` on `*`, merged roles).
- **GitHub OIDC subject claims are immutable-ID format for repos created ≥2026-07-15** (`repo:org@<id>/repo@<id>:…`) — every older trust-policy tutorial silently never matches.
- **Schema rules:** portable type promotions are exactly `int→long`, `float→double`, decimal widening; never reuse a column name (fresh column ID → silent nulls + name-based union welds old/new semantics); `lower_snake_case` enforced (Athena lowercases, PyIceberg is case-sensitive).
- Registry conventions: `TIMESTAMPTZ` always; state machines as `TEXT`+`CHECK` (never enum ordinals — OpenMetadata's frozen `SMALLINT` enum is the cautionary tale); JSONB with generated-column promotion; UUIDv7 PKs + `UNIQUE(namespace,name)`; `deleted_at` soft deletes with partial unique indexes.

## Pitfalls & misconceptions

- "Iceberg tags = dataset releases" — tags preserve schema-as-of-release but **neither Athena nor DuckDB resolves a tag by name** (bigint snapshot IDs only); the registry is the address book, tags are a safety net.
- "expire_snapshots + S3 lifecycle rules = cheap cleanup" — **retracted as a corruption path**: lifecycle rules are blind to Iceberg metadata and can delete files referenced by live snapshots.
- "Aurora Serverless scales to zero, so it's cheapest" — any open connection blocks pausing; paused instances *skip* (not queue) scheduled jobs; always-on floor ≈ $46/mo vs RDS small at ~$26.
- "Adopt the 17.9k-star FastAPI domain-per-package layout" — optimized for many unrelated domains; Artemis is one domain → layer-based split, enforced by import-linter.
- ECS.8 passes a plaintext `DATABASE_PASSWORD` (it greps 3 literal AWS key names); ECS.1 was retired March 2026 but still circulates in templates.

## Open questions

- Spike 1: duckdb-iceberg #805 — PyIceberg column-add crashes attached-catalog DuckDB reads on exactly this stack (workaround: `iceberg_scan`).
- Spike 2: DuckDB writes against Glue REST specifically (docs conflict).
- Spike 3: does Glue managed compaction preserve µs timestamps? If not, Trino enters V1 for compaction.
- ADR-003 flagged gaps: M2M-auth community practice (SigV4/mTLS/IdPs) and Python packaging conventions — deferred behind the `Principal` abstraction and `src/` layout.
