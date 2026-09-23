# Ingest log

Append-only. One entry per ingest:
`## [YYYY-MM-DD] ingest | <title> — Disposition: New|Update|Disputed|No material`
followed by the raw path and any cascade-updated notes.

## [2026-08-27] ingest | LLM-maintained knowledge bases research dossier — Disposition: New
Raw: llm-knowledge-bases/raw/2026-08-27-kb-research-dossier.md
Note: llm-knowledge-bases/llm-maintained-knowledge-bases.md
Cascade: none (first note in theme). Pre-existing artemis/ and demand-graph/ notes
predate the raw/ grounding layer — grandfathered, flagged by lint as [no raw links].

## [2026-09-22] ingest | ECC (affaan-m/ECC) Claude Code plugin — Disposition: New
Raw: claude-code-tooling/raw/2026-09-22-ecc-readme-and-install.md (README excerpts + observed global install record)
Note: claude-code-tooling/ecc-everything-claude-code.md
Cascade: none (new theme). Tracking only — no ECC skills/agents copied into this repo.
