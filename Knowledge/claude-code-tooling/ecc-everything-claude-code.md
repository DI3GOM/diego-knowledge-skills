---
type: topic
topic: ECC (affaan-m/ECC) — Claude Code plugin
updated: 2026-09-22
verified: 2026-09-22
angle: what ECC is, how it is installed on Diego's Mac, and which command to reach for in a new session
sources:
  - https://github.com/affaan-m/ECC
  - https://www.npmjs.com/package/ecc-universal
raw:
  - raw/2026-09-22-ecc-readme-and-install.md
---

# ECC (affaan-m/ECC) — Claude Code plugin

> **In one paragraph:** ECC is an MIT-licensed "agent harness" pack that turns Claude Code into a plan → test → implement → review → verify → remember loop. It ships 68 agents, 292 skills and 94 legacy command shims, plus optional hooks, rules and the AgentShield config scanner. On this Mac it is installed **globally (user scope) as the `ecc@ecc` plugin, with hooks OFF** — so the skills, agents and `/ecc:*` commands are available in every Claude Code session, but nothing runs automatically in the background. Nothing from ECC was copied into this repo; this note only tracks it.

## Current install state (as of 2026-09-22)

| Item | Value |
|---|---|
| Plugin | `ecc@ecc`, Version: 2.2.2, Scope: user, enabled |
| Installed via | `npx -y ecc-universal@2.2.1 install --guided --harness claude --claude-scope user --claude-hooks off --yes` |
| Hooks | `"hooks_enabled": false` in `~/.claude/settings.json` → `pluginConfigs` |
| Plugin files | `~/.claude/plugins/cache/ecc/ecc/2.2.2` (marketplace clone: `~/.claude/plugins/marketplaces/ecc`) |
| Rules packs | none installed (plugins cannot distribute rules; add manually only if wanted) |

- The npm package and the plugin version differ: npm `latest` was 2.2.1, while the plugin pulled
  from the git marketplace reports 2.2.2. The README's pinned `npx ecc-universal@2.2.2` **failed**
  with `No matching version found` — use the npm `latest` instead.

## Which command in which case

Plugin commands are namespaced `/ecc:<name>`; skills can be asked for by name in plain English.

| Situation | Reach for |
|---|---|
| Starting a feature | `/ecc:plan <feature>`, edit/approve the plan, then ask for the `tdd-workflow` skill |
| Fixing a bug | `tdd-workflow` skill: failing test that reproduces it first, then the fix |
| Reviewing fresh code | `/ecc:code-review` (the bare `/code-review` is Claude Code's built-in one) |
| Broken build | `/ecc:build-fix` |
| Cleanup / dead code | `/ecc:refactor-clean` |
| Python-specific review (e.g. M4R) | `/ecc:python-review` |
| Security audit of code or agent config | `/ecc:security-scan` |
| Context feels bloated | `/ecc:context-budget` |
| Ending / resuming a long session | `/ecc:save-session` → `/ecc:resume-session` |
| See what is installed | `/plugin list ecc@ecc` |

## Core concepts

- **Skills** — workflows loaded only when a task needs them (cheap on context).
- **Agents** — scoped subagents with their own context (planner, code-reviewer, build-error-resolver…).
- **Hooks** — scripts fired on tool events, run outside the model context. Disabled here.
- **Rules** — always-loaded standards; install selectively because they cost context every session.

## Why hooks are off

The installer's own dry-run warning says the `standard` profile can "Send transcript-derived
conversation text to an external LLM", "Automatically format or otherwise modify project source
files", and "Automatically deny or alter Edit, Write, Bash, and configuration operations". The
`minimal` profile printed the same six capabilities. Decision 2026-09-22: keep hooks off; lose
auto-formatting, session memory/"instincts" and continuous learning in exchange for no background
behavior. The hook scripts stay registered but check `hooks_enabled` (env
`CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED`) and do nothing when it is false.

## Maintenance

- **Update / change scope / turn hooks on:** rerun the guided setup, e.g.
  `npx ecc-universal@latest setup`, or the same `install --guided` command with
  `--claude-hooks standard`. Rerunning is the supported way to change the hook profile.
- **Uninstall:** remove the plugin from Claude Code (`/plugin` → uninstall `ecc@ecc`); ECC only
  removes files recorded in its install-state.
- **Health:** `npx ecc-universal@latest doctor` / `list-installed`.

## Pitfalls & misconceptions

- **Do not stack install methods.** Guided setup and `/plugin install ecc@ecc` produce the same
  plugin; doing both (or adding a full manual install) duplicates skills, commands and hooks.
- **Official sources only:** GitHub `affaan-m/ECC`, npm `ecc-universal` / `ecc-agentshield`, plugin
  slug `ecc@ecc`, ecc.tools. The README warns re-uploads "may contain malware".
- `ecc-install` is a binary inside `ecc-universal`, not its own npm package.
- Global scope means ECC's skills/agents are offered in every session, including M4R — overlap with
  existing personal skills (research, code review) is possible; prefer whichever is more specific.

## Open questions

- Is ECC's `/ecc:plan` + `tdd-workflow` worth it on M4R pipeline work vs the `pipelinehelper` skill?
- Would the `python` rules pack help M4R enough to justify its always-loaded context cost?

## See also

- [llm-maintained-knowledge-bases](../llm-knowledge-bases/llm-maintained-knowledge-bases.md) — ECC's
  "instincts"/memory is a different take on persisted agent knowledge.
