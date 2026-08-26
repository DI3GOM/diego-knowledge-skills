---
name: creating-skills
description: Guidelines and format specification for authoring high-quality agent skills (SKILL.md files). Use whenever the user wants to create a new skill, edit or improve an existing skill, review a skill, or asks about skill structure, frontmatter, descriptions, or best practices — "make a skill", "write a SKILL.md", "why isn't my skill triggering", "improve this skill".
---

# Creating Skills

How to write a skill that actually gets triggered, loads cheaply, and changes agent behavior for the better. For exact format rules (frontmatter fields, limits, file locations) read `references/format-spec.md`.

## Before writing anything

**The kill criterion:** if the agent already handles the task well without the skill, the skill adds nothing. Run the task once *without* a skill and note the exact failures — those failures are the skill's real content. Don't create skills for one-off tasks, well-documented standard practice, or anything enforceable by a linter/script (automate those instead).

**Scope like a function.** One coherent capability per skill. Too narrow → several skills must load for one task and conflict. Too broad → it never triggers precisely. "Query the DB and format results" is one skill; adding "…and administer the DB" is two.

## The description is the product

The `name` + `description` are the only part loaded into every session (~100 tokens); the agent picks from all its skills using nothing else. Rules:

- **Third person.** "Extracts key knowledge from a topic…" — never "I can help you…"
- **What it does + when to use it**, dense with concrete keywords, file extensions, and trigger phrases users would actually type.
- **Be pushy.** Agents undertrigger skills. End with an explicit trigger list: "Use whenever the user mentions X, Y, Z — even if they don't explicitly ask for it."
- **Never summarize the workflow's shape** (step counts, sequence). A description saying "does one review pass" gets *followed instead of the body being read*. Describe domain and scope, not procedure.

## Writing the body

**The context window is a public good.** Once loaded, every token competes with the actual task. For each line ask: *would the agent get this wrong without it?* If no, cut. Assume the model is already smart — explain what's non-obvious, not what a PDF is.

**Budgets:** body under 500 lines (ideally far under); split anything bulky into `references/` files, one level deep, with an explicit load condition: "Read `references/errors.md` if the API returns non-200" beats "see references/ for details". Information lives in SKILL.md *or* a reference file, never both.

**Calibrate freedom per section.** Narrow bridge (fragile, sequence-dependent — migrations, packaging): exact commands, "run exactly this". Open field (many valid paths — reviews, writing): heuristics and direction. Most skills mix both. Prefer explaining *why* over stacking MUSTs and NEVERs — an all-caps ALWAYS is a yellow flag that a reason is missing.

**One default, one escape hatch.** "Use pypdf; drop to pdfplumber for scanned files" — never a menu of five options.

**Gotchas are the highest-value section.** Environment facts that defy reasonable assumptions ("the `/health` endpoint returns 200 even when the DB is down — use `/ready`") belong in SKILL.md itself, not a reference file. Every time an agent makes a mistake you correct, add it here — this is the main iteration lever.

**Scripts** (`scripts/`): bundle one when you see the agent re-deriving the same code across runs. Say explicitly whether to *run* it or *read* it. Handle errors inside the script; don't make the agent improvise. No unexplained constants.

## Testing

1. **Baseline first:** give a fresh agent the task *without* the skill; record exact failures and rationalizations.
2. Write the minimal skill that fixes those.
3. Test with a **fresh agent instance** (not the one that helped write it) on ≥3 realistic prompts — including near-miss prompts that should *not* trigger it.
4. Watch for signals: agent explores unexpectedly → structure unclear; never opens a bundled file → cut it or signal it better; leans on one reference file constantly → move that content into SKILL.md.
5. Generalize from feedback — if the skill only works for the three test examples, it's overfit.

## Checklist before shipping

- [ ] Folder name matches `name` frontmatter; lowercase-hyphens, ≤64 chars
- [ ] Description ≤1024 chars, third person, what + when + trigger keywords
- [ ] Body <500 lines; references one level deep with load conditions
- [ ] No time-sensitive phrasing ("currently", "as of recently")
- [ ] Consistent terminology (one name per concept)
- [ ] Only portable frontmatter fields unless intentionally Claude-Code-only (see format spec)
- [ ] Tested against a fresh agent with ≥3 prompts, including should-NOT-trigger cases
