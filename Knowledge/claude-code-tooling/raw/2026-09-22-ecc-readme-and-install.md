# ECC (affaan-m/ECC) — source snapshot, 2026-09-22

Immutable. Excerpts of https://github.com/affaan-m/ECC README (HEAD as fetched 2026-09-22)
plus the observed local install record on Diego's Mac. Excerpts only — not a copy of the repo.

---

## A. README excerpts (verbatim)

> **Official sources only.** Install ECC only from verified channels: the GitHub repository [github.com/affaan-m/ECC](https://github.com/affaan-m/ECC), the npm packages [`ecc-universal`](https://www.npmjs.com/package/ecc-universal) and [`ecc-agentshield`](https://www.npmjs.com/package/ecc-agentshield), the [GitHub App](https://github.com/apps/ecc-tools), the plugin slug `ecc@ecc`, and the project website [ecc.tools](https://ecc.tools). Third-party re-uploads and unofficial mirrors are not maintained or reviewed by the project and may contain malware.

## Install with Claude Code

Use the [guided setup](#install-ecc) or [native plugin commands](#claude-code-details). Both install the same `ecc@ecc` plugin. Choose one and do not stack a full manual Claude install on top.


# ECC

Your agent can write code, but ECC gives it a coordinated engineering system and toolbox: it plans before it builds, verifies changes with tests, reviews its own work from a fresh context, remembers what matters, and turns repeated wins into reusable skills and workflows.

```text
plan -> test -> implement -> review -> verify -> remember -> improve
```

Instead of rebuilding that process in every prompt, you install it once and make it part of how your agent works.

> Optimize the context window. Persist everything else.

ECC is MIT-licensed open source. It works best with Claude Code today, has a supported Codex sync path, and provides capability-limited adapters for Cursor, OpenCode, Gemini, Zed, GitHub Copilot, Antigravity, Qwen, and other harnesses. See the [support status matrix](#platform-support) before assuming feature parity.

Access to 68 agents, 292 skills, and 94 legacy command shims, plus hooks, rules, memory, continuous learning, and AgentShield security scanning. The agents are specialized for planning, review, build repair, security, architecture, and domain work.

| Included         |       Count | What it gives you                                                                    |
| ---------------- | ----------: | ------------------------------------------------------------------------------------ |
| Agents           |   68 agents | Planning, review, build repair, security, architecture, and domain work              |
| Skills           |  292 skills | TDD, research, security, docs, frontend, data, ML, operations, and more              |
| Commands         | 94 commands | Convenient entry points while ECC moves to a skills-first surface                    |

## Install ECC

> [!IMPORTANT]
> ECC 2.2 includes guided package setup for Claude Code, Codex, and Kimi Code.
> The universal package requires Node.js 18 or newer. Claude plugin setup also
> requires Git and Claude Code 2.1 or newer on `PATH`.

### Recommended: universal guided setup

For Claude Code plugin setup, updates, scope changes, and hook-profile changes:

```bash

### Pick one path only (per harness)

You can use ECC with Claude Code, Codex, and other harnesses at the same time. Choose one install method for each harness:

- **Recommended default:** run the guided Claude plugin setup above
- **Also supported for Claude Code:** use the [native plugin commands](#claude-code-details)
- **Available in release 2.2:** guided package setup for Claude Code, Codex, and Kimi Code
- **Works:** Claude Code plugin + Codex native plugin
- **Works:** Claude Code plugin + the legacy Codex sync flow
- **Avoid:** Claude Code plugin + full Claude manual install
- **Avoid:** Codex sync + Codex marketplace plugin

**Do not stack install methods.** Installing ECC twice into the same harness can duplicate skills, commands, hooks, or configuration; installing it once into multiple harnesses does not.

If you already layered multiple installs and things look duplicated, skip straight to [Reset / Uninstall ECC](#reset--uninstall-ecc).

**Install trouble?** Open the short [install or runtime problem form](https://github.com/affaan-m/ECC/issues/new?template=install-problem.yml), or run `ecc feedback`. ECC never uploads diagnostics automatically.

### Claude Code details

Alternatively, run Claude Code's native plugin commands inside Claude Code:

```text
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```

The native path installs ECC's skills, agents, commands, and plugin-managed hooks. If you choose it, stop there. Do not also run a full manual install into Claude Code.

Claude Code owns these built-in commands, including their errors when a marketplace, plugin, or conflicting scope already exists. ECC cannot intercept that parser. If either native command reports an existing install or scope conflict, use the 2.2 guided setup or resolve the conflicting Claude plugin scope before retrying; do not layer a manual install on top.

After ECC is installed, `/ecc:configure-ecc` is the namespaced in-Claude reconfiguration skill. It delegates to the same safe setup flow, but it is available only after the plugin is installed and cannot replace Claude Code's built-in `/plugin` command during a first install.

Claude Code plugins cannot distribute `rules`, so add only the rule packs you actually want:

```bash
git clone https://github.com/affaan-m/ECC.git

### Reset / Uninstall ECC

If you installed from the universal package, run these commands from the same
project directory used for installation:

```bash
npx ecc-universal@2.2.2 list-installed
npx ecc-universal@2.2.2 doctor
npx ecc-universal@2.2.2 repair
npx ecc-universal@2.2.2 uninstall --dry-run
npx ecc-universal@2.2.2 uninstall
```

From a source checkout, inspect the managed state before reinstalling:

```bash
node scripts/ecc.js list-installed
node scripts/ecc.js doctor
node scripts/ecc.js repair
node scripts/ecc.js uninstall --dry-run
```

For a direct source-checkout uninstall:

```bash
node scripts/uninstall.js --dry-run
node scripts/uninstall.js
```

If you are leaving, the uninstall command prints an optional [20-second feedback form](https://github.com/affaan-m/ECC/issues/new?template=quick-feedback.yml). It is a public GitHub issue, never blocks uninstall, and ECC does not upload diagnostics. You can also run `ecc feedback` at any time to see the problem, feedback, and feature routes.

Plugin users should remove the plugin from Claude Code, then delete only the rule folders they manually copied and no longer want. ECC only removes files recorded in its install-state. It does not claim unrelated files in your harness directories.

If you stacked methods, clean up in this order:

1. Remove the Claude Code plugin install.
2. Run the ECC uninstall command from the project directory that contains the managed install-state.
3. Delete any extra rule folders you copied manually and no longer want.
4. Reinstall once, using a single path.
</details>


## Start Using ECC

Start with the workflow you need, not the full catalog.

| What you are doing | Start here |
|---|---|
| Building a feature | `/ecc:plan "describe the feature"`, then `tdd-workflow` |
| Fixing a bug | Reproduce it with a failing test, then use `tdd-workflow` |
| Reviewing new code | `/code-review` for a fresh-context review |
| Repairing a build | `/build-fix` |
| Cleaning a codebase | `/refactor-clean` |
| Checking context pressure | `/context-budget` |
| Ending a long session | `/save-session` or `/learn-eval` |
| Resuming later | `/resume-session` |
| Auditing agent config | `/security-scan` with a reviewed scanner, or installed `agentshield scan --path .` |


## Why Choose ECC?

| Without a system                                        | With ECC                                                              |
| ------------------------------------------------------- | --------------------------------------------------------------------- |
| Plans disappear into chat history                       | Plans become editable artifacts before implementation starts          |
| "Please use TDD" is an instruction the model may forget | TDD becomes a gated RED -> GREEN -> REFACTOR workflow with evidence   |
| The same context writes and reviews the code            | A fresh-context reviewer looks for regressions and blind spots        |
| Memory means saving an enormous transcript              | Sessions are distilled into summaries, instincts, and reusable skills |
| Quality checks depend on reminders                      | Hooks can enforce deterministic checks outside the prompt             |
| Agent configuration is trusted by default               | AgentShield scans the harness itself as an attack surface             |

### Skills keep the context focused

Rules, skills, agents, and hooks solve different problems. Keeping those jobs separate is how ECC adds capability without dumping the entire repository into every session.

| Concept | What it does | Context behavior |
|---|---|---|
| Skills | Reusable workflows such as TDD, security review, or deep research | Loaded when the task needs them |
| Agents | Scoped workers with their own context and tool permissions | Isolate planning, implementation, and review |
| Rules | Durable project or language standards | Always loaded, so install them selectively |
| Hooks | Scripts triggered by harness events | Run outside the model context |
| Instincts | Patterns learned from real sessions with confidence scores | Recalled when relevant |


---

## B. npm registry (`npm view ecc-universal`, 2026-09-22)

```
version = '2.2.1'
dist-tags = { next: '2.0.0-rc.1', latest: '2.2.1', staged: '2.2.1' }
maintainers = 'cogsec <me@affaanmustafa.com>'
repository.url = 'git+https://github.com/affaan-m/ECC.git'
```

`npx ecc-universal@2.2.2 ...` (the README's pinned command) failed:
`npm error notarget No matching version found for ecc-universal@2.2.2.`

## C. Installer hook warning (dry run of `install --guided --harness claude --claude-hooks standard`)

```
Claude hook profile 'standard' enables automation that can:
  1. Automatically format or otherwise modify project source files.
  2. Rewrite requested commands and start, replace, or terminate processes.
  3. Send transcript-derived conversation text to an external LLM.
  4. Probe MCP endpoints and launch, reconnect, or terminate MCP processes.
  5. Automatically deny or alter Edit, Write, Bash, and configuration operations.
  6. Persist session, observation, governance, notification, and cost records.
Choose '--claude-hooks off' to install without automatic hook behavior.
```

The 'minimal' profile dry run printed the same six capabilities.

## D. Install performed 2026-09-22

Command:
```
npx -y ecc-universal@2.2.1 install --guided --harness claude --claude-scope user --claude-hooks off --yes
```
Output: `ECC configured for Claude Code.`

`claude plugin list`:
```
❯ ecc@ecc
    Version: 2.2.2
    Scope: user
    Status: ✔ enabled
```

~/.claude/settings.json (relevant keys):
```
"enabledPlugins": { "ecc@ecc": true },
"extraKnownMarketplaces": { "ecc": { "source": { "source": "git", "url": "https://github.com/affaan-m/ECC.git" } } },
"pluginConfigs": { "ecc@ecc": { "options": { "hooks_enabled": false, "hook_profile": "standard" } } }
```

Plugin files: ~/.claude/plugins/cache/ecc/ecc/2.2.2 ; marketplace clone: ~/.claude/plugins/marketplaces/ecc

Hook kill switch (scripts/lib/hook-flags.js, `areHooksEnabled`): reads `ECC_HOOKS_ENABLED`, then
`CLAUDE_PLUGIN_OPTION_HOOKS_ENABLED`, then managed config; default true. plugin.json userConfig
`hooks_enabled` description: "Disable this to keep skills and commands without local hook automation."
