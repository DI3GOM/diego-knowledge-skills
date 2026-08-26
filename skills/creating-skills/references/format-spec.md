# Agent Skill Format Specification (condensed)

Condensed from the normative spec at https://agentskills.io/specification and
Claude Code docs (https://code.claude.com/docs/en/skills). As of 2026-08.

## Contents
- Directory structure
- Frontmatter fields (portable)
- Claude-Code-only fields
- Progressive disclosure levels
- Where skills live
- Naming rules
- Validation

## Directory structure

```
skill-name/
├── SKILL.md          # REQUIRED — frontmatter + instructions
├── scripts/          # optional — executable code (run, not read; stdout only enters context)
├── references/       # optional — docs loaded on demand
└── assets/           # optional — files used in the OUTPUT (templates, fonts, images)
```

Only `SKILL.md` is required. Subdirectory names are convention, not enforced.

## Frontmatter — the 6 portable fields

| Field | Required | Constraint |
|---|---|---|
| `name` | Yes | ≤64 chars; `a-z0-9-` only; no leading/trailing/double hyphen; **must equal the folder name**; no "anthropic"/"claude" |
| `description` | Yes | ≤1024 chars, non-empty, no XML tags. What it does AND when to use it |
| `license` | No | Short license name or pointer to bundled LICENSE file |
| `compatibility` | No | ≤500 chars, environment requirements. Rarely needed |
| `metadata` | No | Arbitrary string→string map |
| `allowed-tools` | No | Space-separated pre-approved tools. Experimental |

claude.ai uploads, the Skills API, and packaging tools reject any other key. Stick to these six for portability (the spec is implemented by ~45 clients: Claude Code, Codex, Copilot, Cursor, Gemini CLI, …).

## Claude-Code-only fields (break portability)

`when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`,
`user-invocable`, `disallowed-tools`, `model`, `effort`, `context: fork`,
`agent`, `background`, `hooks`, `paths`, `shell`.

Useful ones: `disable-model-invocation: true` (slash-command only),
`user-invocable: false` (model only, hidden from `/` menu),
`paths:` (auto-load only when touching matching files).

## Progressive disclosure

| Level | Loaded | Cost | Content |
|---|---|---|---|
| 1 | Always, at startup | ~100 tokens/skill | `name` + `description` |
| 2 | On trigger | keep <5k tokens / <500 lines | SKILL.md body |
| 3 | On demand | zero until read | `references/*.md`; `scripts/*` executed |

Rules:
- Reference files must be **one level deep** from SKILL.md — no chains.
- Reference files >100 lines need a table of contents at the top.
- Relative paths from the skill root, forward slashes only.
- Tell the agent *when* to read each reference file.
- SKILL.md content stays in context for the whole session once loaded — write standing instructions, not one-time steps.

## Where skills live (Claude Code)

| Scope | Path |
|---|---|
| Personal (all projects) | `~/.claude/skills/<name>/SKILL.md` |
| Project | `.claude/skills/<name>/SKILL.md` |
| Plugin | `<plugin>/skills/<name>/SKILL.md` |

Precedence: enterprise > personal > project. Codex/Copilot/Gemini also read `~/.agents/skills/`.

## Naming

Prefer gerund form: `processing-pdfs`, `extracting-knowledge`, `creating-skills`.
Avoid: `helper`, `utils`, `tools`, generic nouns.
Name by what the skill *does* or its core insight.

## Validation

- `skills-ref validate ./my-skill` (from github.com/agentskills/agentskills)
- Anthropic's `skill-creator` skill bundles `quick_validate.py` and an eval loop
  (github.com/anthropics/skills — 19 official example skills worth reading)
