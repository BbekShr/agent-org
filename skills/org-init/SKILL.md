---
name: org-init
description: Bootstrap a CEO-led agent org for the current project. Scans the codebase, interviews the user briefly, then generates tailored specialist agents (.claude/agents/), a /<project>-ceo orchestrator skill, org memory (.claude/ceo/), guard hooks, and seed evals, sized to the project and starting at the autonomy level its verification bar can support. Invoke as /org-init (new org), /org-init adopt (normalize an existing hand-built CEO/agents setup without losing its content), or /org-init upgrade (re-sync a generated org with the latest templates, preserving local edits). Use when the user wants "a CEO and agents for this repo", "an agent team", "orchestration like my other project", or to set up autonomous maintenance.
---

# org-init: generate an agent org for this project

You are building a small company of agents for the project in the current working directory: a
CEO skill that orchestrates, specialist agents that each own a perimeter or a lens, and the memory,
guards and evals that let the org earn autonomy over time.

**The core principle you are encoding:** autonomy comes from verification + constraints + evals +
orchestration, not from better prompts. Start constrained and local, prove correctness, then
scale. Read `references/principles.md` in full before generating anything. Every generated file
must carry those rules, and you are expected to understand why each exists.

Files in this skill (resolve against this skill's directory):
- `references/principles.md`: the rules and the incidents behind them. Copied into the project.
- `references/autonomy.md`: the L0-L4 trust curve. Copied into the project.
- `references/roster.md`: which agents to generate and the signals that call for each.
- `templates/`: agent, CEO, org-state, hook, and schedule templates with `{{PLACEHOLDERS}}`.
- `references/placeholders.md`: what goes in every placeholder, with size-based defaults.

## Mode

- **`/org-init`** (default): new org. If `.claude/ceo/org.json` already exists, stop and offer
  `upgrade`. If `.claude/agents/` or a `*-ceo` skill exists without `org.json`, offer `adopt`.
- **`/org-init adopt`**: see "Adopt" below.
- **`/org-init upgrade`**: see "Upgrade" below.

## Phase 0: Preflight
1. Confirm a git repo (`git rev-parse --show-toplevel`). Not a repo → offer `git init` and stop
   until the user agrees.
2. Record: base branch (`git symbolic-ref refs/remotes/origin/HEAD` or `main`), whether `gh` is
   authenticated, existing `CLAUDE.md`/`AGENTS.md`, `.claude/settings.json`, `.claude/agents/`,
   `.claude/skills/`, and the list of installed skills in this session (critics can lean on them:
   `taste-skill`, `ponytail`, `dataviz`, `ui-ux-pro-max`, `frontend-design`, ...).
3. Work on a branch: `org/bootstrap-<YYYY-MM-DD>`. Never write the org onto the base branch directly.

## Phase 1: Discover (parallel, read-only: ONE message, 4 Explore agents)

Brief each with the repo root as an absolute path and ask for conclusions with `file:line`, not
dumps. Each returns the section named.

1. **Stack & commands**: languages, frameworks and versions, package manager; the exact commands
   for install, dev server (and its port), typecheck, lint, format check, unit tests, e2e tests,
   build; which of those currently exist; CI workflows and what they actually enforce on a PR;
   the files that configure each gate (tsconfig, lint config, test config, size budgets).
   Size: rough LOC and contributor count (`git shortlog -sn | head`).
2. **Architecture & perimeters**: the top-level layout, the natural seams (client/server,
   app/library, jobs/bots, AI boundary, infra), proposed perimeters as globs with a one-line
   rationale each, the core user journeys (3-5, named as flows), and whether features are
   collocated or scattered.
3. **Risk surface**: auth/session layer, role checks and their canonical pattern, input
   validation helpers, where secrets are read, rendering of untrusted content, outbound fetchers,
   write paths and migrations, deploy trigger (does merging deploy?), anything that costs money
   per call, documented design decisions that look like bugs (fail-open limiters, deliberate
   cache gaps), and the files that should be protected paths.
4. **Conventions & history**: existing rules in CLAUDE.md/AGENTS.md/CONTRIBUTING, error-handling
   and validation idioms, test locations and style, comment density; from `git log`: the last
   ~30 commits whose message says fix/bug/regression, as `sha | subject | files` (this seeds evals),
   recurring defect classes, and any reverts.

While they run, do nothing else in the tree.

## Phase 2: Verification-bar check and constraint audit (you, from the reports)

1. **Run the cheap gates once yourself** (typecheck, lint, unit tests: whichever exist) on the base
   branch. Record pass/fail and counts. These are the org's baseline facts.
2. **Grade the verification bar:** STRONG (typed + lint + tests green + app runnable) · PARTIAL ·
   WEAK (no tests, or no way to run). This sets the starting autonomy level (`autonomy.md`):
   WEAK → L0, otherwise L1. Never start higher.
3. **Constraint audit:** for each critical rule you found (written or implied by the risk
   surface), note the strongest layer that currently enforces it: architecture / CI / type-lint /
   review-only / nothing. Rules at review-only or nothing become seed `P` backlog items: "enforce
   <rule> at <stronger layer>", with acceptance criteria. Missing gates (no typecheck in CI, no
   test runner) become seed items too, ranked first.

## Phase 3: Interview (ONE AskUserQuestion call, ≤4 questions, recommended option first)

Ask only what you can't infer. Typical set:
1. **North Star & priority**: offer two or three drafted one-liners from discovery ("<what the
   project must do>, priority Correct > Fast > Beautiful") plus Other.
2. **Org size**: small / standard / full with your recommendation from `roster.md` and the measured LOC.
3. **Autonomy target**: where the user wants to get to (L1 PRs I review · L2 nightly runs ·
   L3 agents merge green PRs · L4 cloud). Explain that the org *starts* at the level the
   verification bar supports and climbs by evidence.
4. **Optional modes**: multi-select from what applies (`e2e` if the app is runnable; `discover`;
   `rnd`; `issues` if the repo takes public issues).

## Phase 4: Design the org, show it, get a yes

Using `roster.md`, produce and present (as one compact message, not a file dump):
- the roster table: agent, access (editor / report-only), perimeter or lens, model tier,
  and the discovery signal that justified it;
- the ownership map (globs → owner) with a default owner, plus the dependency order for findings
  that span perimeters (e.g. "backend first");
- the verification bar table and which gates are "cheap" (safe in parallel worktrees);
- protected paths and gate files;
- the objective function with this project's journeys named;
- starting autonomy level, target, and why;
- seed backlog items (from the constraint audit and the bar check), max ~8.

Model tiers: top = `opus` (or the newest top model available), mid = `sonnet`, small = `haiku`,
unless the user named others. Ask for a yes or edits. Apply edits and proceed. Don't re-ask.

## Phase 5: Generate

Slug = short lowercase project name (from package name or directory). Fill every template
placeholder. **No `{{` may survive in a generated file**; `/org-doctor` fails on one.
HTML comments in templates that describe what to fill (`<!-- From discovery: ... -->`) are
instructions to you: replace them with the content, then delete the comment.

| Write | From |
|---|---|
| `.claude/agents/<slug>-<role>.md` per roster entry | `templates/agents/<role>.md`; editors from `editor.md`, critics from `critic.md`. Paste `_contract.md`'s BOOT and REPORT_CONTRACT blocks where `{{BOOT}}`/`{{REPORT_CONTRACT}}` appear |
| `.claude/skills/<slug>-ceo/SKILL.md` | `templates/ceo/SKILL.md`, with the chosen `templates/ceo/modes/*.md` pasted at `{{EXTRA_MODES}}` |
| `.claude/ceo/org.json` | `templates/org/org.json`, filled with the real gates, gate files, protected paths, agents (name, access, role, perimeter globs), modes, and `guard.stop_check` (the cheapest meaningful check, e.g. typecheck, or `""` if none) |
| `.claude/ceo/{README,backlog,feature-map}.md`, `memory/*`, `learnings/*` | `templates/org/` (`feature-map.md` only for UI projects) |
| `.claude/ceo/.gitignore` | `templates/org/gitignore` |
| `.claude/ceo/PRINCIPLES.md`, `.claude/ceo/AUTONOMY.md` | copy `references/principles.md`, `references/autonomy.md` verbatim |
| `.claude/ceo/evals/` | see Phase 6 |
| `.claude/hooks/org_guard.py` | `templates/hooks/org_guard.py` (verbatim) |
| `.claude/ceo/bin/org_doctor.py` | copy `../org-doctor/scripts/org_doctor.py` verbatim, so preflight, headless and cloud runs never depend on where this plugin is installed |
| `.claude/settings.json` | **merge** `templates/hooks/settings.snippet.json` into the existing file: keep every existing key and hook; never replace the file |
| `CLAUDE.md` | **append** `templates/claude-md-section.md` as a new section (create the file if absent). Never rewrite existing content |
| `.claude/ceo/schedule/run-headless.sh` | only if the target is ≥L2; mark executable |

Fill content from discovery, never from generic filler: perimeters are real globs that match
files (`git ls-files '<glob>' | head` proves each one), commands are the real commands, the
security surface names real files. Keep each agent tight: the best agents in the source orgs
are 40-140 lines. If a section has nothing project-specific to say, cut it rather than pad it.

## Phase 6: Seed evals

Create `.claude/ceo/evals/cases/` with 1-3 known-answer cases per editor and per hunting/review
role, preferring cases mined from git history (Phase 1 report 4). Format in the `org-eval` skill;
if that skill is unavailable, use this:

```
---
id: <slug>-<n>
agent: <agent-name>
kind: find-the-bug | fix-the-bug | gate
base: <parent sha of the real fix commit>
---
## Task (what the agent is told; neutral, no hint at the answer)
## Expected (what a correct answer contains: file, mechanism, or a test that must pass)
## Rubric (3-5 scored criteria, 0-2 each)
```

A good "find" case: the parent of a real fix commit, the agent told to audit the touched module,
expected = the defect the fix addressed. A good "gate" case: a release-manager run on a commit
known to fail a gate.

## Phase 7: Validate (don't ship an org you haven't checked)

1. Run `/org-doctor` (or `python3 <org-doctor skill dir>/scripts/org_doctor.py <repo root>`). Fix
   every error.
2. Test the guard: pipe `{"tool_input":{"command":"git stash"}}` into
   `python3 .claude/hooks/org_guard.py bash` and expect exit 2; same with a harmless `git status`
   expecting exit 0; same with an `edit` payload for one gate file expecting exit 2.
3. Smoke-test one agent: dispatch the release manager (read-only) on the base branch with a
   "run the cheap gates and report" brief. Confirm its report follows the contract and that it
   resolved `.claude/ceo/...` against the repo root.
4. Write the baseline into `memory/codebase.md` and the bootstrap line into `memory/retros.md`.

## Phase 8: Hand off

Commit on the bootstrap branch (one commit for agents, one for CEO+state, one for hooks/settings/
CLAUDE.md, so each can be reviewed alone). Ask before pushing or opening a PR: those are
outward-facing. Then tell the user, briefly: the roster, the starting level and what would earn
the next one, the first command to run (`/<slug>-ceo audit`), and the kill switch.

## Adopt (existing hand-built org)

For a repo that already has a CEO skill and agents (e.g. `.claude/ceo/backlog.md`,
`.claude/agents/<slug>-*.md`): **preserve content, add structure.** Never delete or rewrite an
existing agent's domain knowledge, backlog, learnings, or reports.
1. Inventory what exists and map it onto the layout above (backlog, learnings, reports, PAUSE,
   ownership map, modes).
2. Generate only what's missing: `org.json` (derived from the existing skill and agents),
   `AUTONOMY.md`, `PRINCIPLES.md`, `memory/scorecard.md` (backfilled from `gh pr list` of past CEO
   PRs if possible), the guard hook (merged alongside any existing hooks, never replacing them),
   and seed evals.
3. For the CEO skill and each agent, produce a **gap report**: principles the existing file lacks
   (e.g. no failure-scenario bar, no freeze-the-tree rule, no autonomy gating). Propose each gap
   as a small, separate edit, and apply only the ones the user accepts.
4. The starting autonomy level for an adopted org can be backfilled from its real PR history
   using the promotion criteria. State the evidence.

## Upgrade (re-sync with newer templates)

Read `org.json` → `agent_org_version`. For each generated file, diff the current file against
what the OLD template would have produced and against the NEW template. Keep the project's own
edits; apply only the template changes. Show the user the template-side diff before writing.
Bump `agent_org_version`. Never touch backlog, memory, learnings, reports, or evals content.

## Never

Push, open PRs, or create GitHub repos without asking. Overwrite an existing CLAUDE.md, settings
file, agent, or skill. Start above the autonomy level the verification bar supports. Generate an
agent whose perimeter globs match no files. Leave a `{{` placeholder in a generated file.
