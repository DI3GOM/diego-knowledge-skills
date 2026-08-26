# diego-knowledge-skills

Personal repository for organized knowledge and reusable agent skills.

```
├── Knowledge/          # distilled, source-grounded notes — one file per topic
└── skills/             # agent skills — one folder per skill, SKILL.md inside
```

## Skills

| Skill | What it does |
|---|---|
| [extracting-knowledge](skills/extracting-knowledge/) | Distill the most important knowledge about a topic into a structured, sourced note in `Knowledge/` |
| [creating-skills](skills/creating-skills/) | Guidelines + format spec for authoring high-quality agent skills |
| [debate](skills/debate/) | Antagonistic design debate — stress-test a spec with advocate, skeptic, and practitioner agents |
| [llm-council](skills/llm-council/) | Run a decision through a council of 5 AI advisors with anonymous peer review (Karpathy's LLM Council) |
| [research](skills/research/) | Preliminary research on a topic → research outline |
| [research-add-fields](skills/research-add-fields/) | Add field definitions to an existing research outline |
| [research-add-items](skills/research-add-items/) | Add items (research objects) to an existing research outline |
| [research-deep](skills/research-deep/) | Launch an independent deep-research agent per outline item |
| [research-report](skills/research-report/) | Summarize deep-research results into a markdown report |

## Installing a skill

Copy the skill folder into Claude Code's personal skills directory:

```bash
git clone git@github.com:DI3GOM/diego-knowledge-skills.git
cp -r diego-knowledge-skills/skills/<skill-name> ~/.claude/skills/
```

Or with the [skills.sh](https://skills.sh) CLI (works for Claude Code, Codex, Cursor, and ~30 other agents):

```bash
npx skills add DI3GOM/diego-knowledge-skills --skill <skill-name>
```

## Skill format

A skill is a folder whose name matches its `name` field, containing a single
required file, `SKILL.md`, with YAML frontmatter:

```yaml
---
name: my-skill            # ≤64 chars, lowercase + hyphens, = folder name
description: What it does AND when to use it, with trigger keywords.  # ≤1024 chars
---
# Instructions the agent follows when the skill triggers
```

Optional subfolders: `references/` (docs loaded on demand), `scripts/`
(executable code), `assets/` (templates/files used in output). Keep `SKILL.md`
under 500 lines and push details into `references/`.

Full guidelines live in the [creating-skills](skills/creating-skills/) skill;
the condensed spec is in
[creating-skills/references/format-spec.md](skills/creating-skills/references/format-spec.md).
Normative spec: [agentskills.io/specification](https://agentskills.io/specification).

## Adding a new skill

1. Trigger the `creating-skills` skill ("make a skill for …") and follow it.
2. Put the finished folder in `skills/`.
3. Add a row to the table above.
4. Copy it to `~/.claude/skills/` to use it locally.
