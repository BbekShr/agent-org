---
name: org-init
description: Bootstrap a CEO-led agent org for the current project. Scans the codebase, interviews the user briefly, then generates tailored specialist agents (.claude/agents/), a /<project>-ceo orchestrator skill, a /<project>-verify skill that runs and inspects the real software, org memory and rules (.claude/ceo/), guard hooks, and seed evals, sized to the project and starting at the autonomy level its verification bar can support. Invoke as /org-init (new org), /org-init adopt (normalize an existing hand-built CEO/agents setup without losing its content), or /org-init upgrade (re-sync a generated org with the latest templates, preserving local edits). Use when the user wants "a CEO and agents for this repo", "an agent team", "orchestration like my other project", or to set up autonomous maintenance.
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
- `references/skills.md`: which installed skills (ponytail, taste-skill, Pstack, framework skills,
  ...) each role loads, and how they're wired.
- `templates/playbooks/`: per-task-kind playbooks (bug fix, perf, feature, refactor, security,
  upgrade, test gap).

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
   `.claude/skills/`, and the list of installed skills in this session, with their **exact names**.
   Match them against `references/skills.md`; Phase 1 decides which matches the project needs.
3. Work on a branch: `org/bootstrap-<YYYY-MM-DD>`. Never write the org onto the base branch directly.

## Phase 1: Discover (parallel, read-only: ONE message, 4 Explore agents)

Brief each with the repo root as an absolute path and ask for conclusions with `file:line`, not
dumps. Each returns the section named.

1. **Stack & commands**: languages, frameworks and versions, package manager; the exact commands
   for install, dev server (and its port), typecheck, lint, format check, unit tests, e2e tests,
   build; which of those currently exist; CI workflows and what they actually enforce on a PR;
   the files that configure each gate (tsconfig, lint config, test config, size budgets).
   Size: rough LOC and contributor count (`git shortlog -sn | head`).
   **Project kind:** web app / mobile app / desktop app / service-API / library / CLI-TUI /
   prompt-product (logic lives in prompt files an agent follows), possibly several.
   **Runtime eyes and hands:** how an agent could run and inspect it for real: dev server and
   port, seed/test accounts in fixture files, e2e harness, browser driving (Playwright, the
   built-in browser pane), simulator/emulator tooling, profilers and trace tooling (Chrome DevTools
   protocol, `--cpu-prof`, Instruments, pprof), log locations. Say what's missing.
2. **Architecture & perimeters**: the top-level layout, the natural seams (client/server,
   app/library, jobs/bots, AI boundary, infra), proposed perimeters as globs with a one-line
   rationale each, the core user journeys (3-5, named as flows), and whether features are
   collocated or scattered.
3. **Risk surface**: auth/session layer, role checks and their canonical pattern, input
   validation helpers, where secrets are read, rendering of untrusted content, outbound fetchers,
   write paths and migrations, deploy trigger (does merging deploy?), anything that costs money
   per call, documented design decisions that look like bugs (fail-open limiters, deliberate
   cache gaps), and the files that should be protected paths.
   **Shipped artifacts:** does any mechanism copy repo files to end users (a self-updater's
   file list, npm `files`/published package, a Docker image, a release bundle)? Does it include
   `CLAUDE.md` or anything under `.claude/`? Name the mechanism and its file list. User-data
   paths: files that hold end-user data (never to be read or written by agents).
4. **Conventions & history**: existing rules in CLAUDE.md/AGENTS.md/CONTRIBUTING, error-handling
   and validation idioms, test locations and style, comment density; from `git log`: the last
   ~30 commits whose message says fix/bug/regression, as `sha | subject | files` (this seeds evals),
   recurring defect classes (a class = the same kind of mistake fixed ≥2 times), and any reverts.
   Collocation: is each feature in one place, or smeared across layers joined only by naming?

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
4. **Bans:** for each recurring defect class from report 4, propose the mechanical ban that would
   have prevented it (a lint rule, a harness check, a type, a structural rule), as a `P` item.
   Architecture and CI beat prompting: a class that has recurred is evidence prose didn't work.
5. **Agent-friendliness:** if features are smeared across layers, or contracts are duplicated in
   several files that must be edited together, note it. If it is severe, file one `P` "big-rock"
   item proposing the restructure (collocated features, single source of truth), and don't start it.
6. **Shipped artifacts:** if `CLAUDE.md` or `.claude/` ships to end users, the org must not leak
   into their installs. Then: don't add even the pointer to `CLAUDE.md`, and file a "Needs a human"
   item to exclude `.claude/agents/`, `.claude/ceo/`, `.claude/hooks/org_guard.py`, and the
   generated skills from the shipping mechanism's file list (it's usually a protected path).

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
- seed backlog items (from the constraint audit, bans, and the bar check), max ~8;
- project kind, user-data paths, shipped-artifact handling (Phase 2.6);
- skills wiring: every `references/skills.md` match the project needs (exact installed name →
  the agents that load it, when, the fallback), plus relevant installed skills the registry
  doesn't know (proposed, wired only on a yes). Note any registry skill worth installing that
  isn't installed, as a suggestion; never install it yourself;
- playbooks: whether Pstack is installed (then the playbooks are thin project adapters) or not
  (then they're the full method), and the project specifics for each playbook;
- the verify skill outline: setup, start, drive, inspect, evidence, teardown (from Phase 1's
  runtime report). If the project can't be run or inspected at all, the first seed item builds
  that, and the verify skill says plainly what's missing.

**Feedback (opt-in, off by default).** In the Phase 4 summary, add one line: "Share template
findings with agent-org? Off unless you say yes: findings are always recorded locally in
`.claude/ceo/upstream.md`, and with feedback on, `/org-feedback` drafts issues or PRs you approve
one by one, with project details stripped." Set `feedback.enabled` from the answer; no answer
means `false`. Never turn it on by default or on your own.

Model tiers: top = `opus` (or the newest top model available), mid = `sonnet`, small = `haiku`,
unless the user named others. Ask for a yes or edits. Apply edits and proceed. Don't re-ask.

## Phase 5: Generate

Slug = short lowercase project name (from package name or directory). Fill every template
placeholder. **No uppercase `{{NAME}}` placeholder may survive**; `/org-doctor` fails on one. (A
project's own `{{lowercase}}` template syntax is fine.) Comments starting `<!-- FILL:` are
instructions to you: replace each with content, then delete it (the doctor fails on a leftover).
Other HTML comments (format guidance in backlog/retros) stay. An agent's filename and frontmatter
`name` must match; its catalog role (e.g. `ai-quality-critic`) can differ from its name
(`<slug>-eval-critic`) and is recorded as `role` in `org.json`.

Tailor the report-only checklists to the project kind: a web app's security checklist (authZ,
IDOR, CORS, rate limits) is wrong for a CLI, where the surface is local files, subprocesses,
untrusted input reaching prompts or renderers, and the update/distribution channel. Same for
the release manager (no ports for a library) and the never-list (no "production deploy" for a
local tool; add the project's own: e.g. "never submit an application on the user's behalf").

| Write | From |
|---|---|
| `.claude/agents/<slug>-<role>.md` per roster entry | `templates/agents/<role>.md`; editors from `editor.md`, critics from `critic.md`. Paste `_contract.md`'s BOOT and REPORT_CONTRACT blocks where `{{BOOT}}`/`{{REPORT_CONTRACT}}` appear |
| `.claude/skills/<slug>-ceo/SKILL.md` | `templates/ceo/SKILL.md`, with the chosen `templates/ceo/modes/*.md` pasted at `{{EXTRA_MODES}}` |
| `.claude/skills/<slug>-verify/SKILL.md` | `templates/verify/SKILL.md`: the org's runtime eyes and hands, filled from Phase 1's runtime report. Always generated (for a library: build, run the test suite, run the examples, profile a hot path) |
| `.claude/agents/<slug>-repro.md` | `templates/agents/repro.md`: always generated (it powers `triage`) |
| `.claude/ceo/playbooks/*.md` | `templates/playbooks/`, each "In this project" section filled from discovery: the real test layout, measurement tools, canonical security helpers, upgrade history. All seven, even when Pstack is installed |
| `.claude/ceo/RULES.md` | `templates/org/RULES.md`: the org's rules (verification bar, protected paths, user-data paths, critical rules) |
| `.claude/ceo/org.json` | `templates/org/org.json`, filled with the real gates, gate files, protected paths, agents (name, access, role, perimeter globs), modes, and `guard.stop_check` (the cheapest meaningful check, e.g. typecheck, or `""` if none) |
| `.claude/ceo/{README,backlog,feature-map}.md`, `memory/*`, `learnings/*` | `templates/org/` (`feature-map.md` only for UI projects) |
| `.claude/ceo/.gitignore` | `templates/org/gitignore` |
| `.claude/ceo/upstream.md` | `templates/org/upstream.md` (the local outbox for template findings) |
| `.claude/ceo/PRINCIPLES.md`, `.claude/ceo/AUTONOMY.md` | copy `references/principles.md`, `references/autonomy.md` verbatim |
| `.claude/ceo/evals/` | see Phase 6 |
| `.claude/hooks/org_guard.py` | `templates/hooks/org_guard.py` (verbatim) |
| `.claude/ceo/bin/org_doctor.py` | copy `../org-doctor/scripts/org_doctor.py` verbatim, so preflight, headless and cloud runs never depend on where this plugin is installed |
| `.claude/settings.json` | **merge** `templates/hooks/settings.snippet.json` into the existing file: keep every existing key and hook; never replace the file |
| `CLAUDE.md` | **append** `templates/org/claude-md-pointer.md` (4 lines; create the file if absent). Never rewrite existing content. **Skip entirely if `CLAUDE.md` ships to end users** (Phase 2.6) |
| `.claude/ceo/schedule/run-headless.sh` | only if the target is ≥L2; mark executable. For compound gate commands (`cd x && cmd`), allowlist each part (`Bash(cd x:*)`, `Bash(cmd:*)`) |

Fill content from discovery, never from generic filler: perimeters are real globs that match
files (`git ls-files '<glob>' | head` proves each one) and never cover org files (`.claude/agents`,
`.claude/ceo`, the generated skills: use `except` in `org.json`; the doctor fails on overlap), commands are the real commands, the
security surface names real files. Keep each agent tight: the best agents in the source orgs
are 40-140 lines. If a section has nothing project-specific to say, cut it rather than pad it.

## Phase 6: Seed evals

Create `.claude/ceo/evals/cases/` with at least one known-answer case for every editor and for
the release manager, plus one per hunting/review role where history offers one, preferring cases
mined from git history (Phase 1 report 4). Kinds: hunters/reviewers/specialists get
`find-the-bug`; editors get `fix-the-bug`; the release manager gets `gate`; the repro agent gets
`triage` (a fixed bug: expected verdict ALREADY FIXED in <sha>). Every file a Task names must
exist at the case's `base` (`git cat-file -e <base>:<path>`): a fix that created the file it
fixed can't be audited at its parent. The format is the `org-eval` skill's; summary:

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
4. Confirm `memory/codebase.md` holds the Phase 2 baseline and `memory/retros.md` the bootstrap
   line in the file's `<friction> → <action>` format, naming any friction from this bootstrap.
5. Test that the cheap gates leave the tree clean (`git status --porcelain` empty after them), so
   apply modes won't spuriously fall back to audit.

## Phase 8: Hand off

Commit on the bootstrap branch: (1) agents, (2) CEO + verify skills and everything under
`.claude/ceo/` (state, rules, evals, bin, schedule), (3) hooks, settings, and the `CLAUDE.md`
pointer, so each can be reviewed alone. Ask before pushing or opening a PR: those are
outward-facing. Then tell the user, briefly: the roster, the starting level and what would earn
the next one, the first command to run (`/<slug>-ceo audit`), and the kill switch. Set the
expectation honestly: the first runs are the investment phase (building tests, bans, the verify
skill, evals) and feel slow; throughput compounds once the org has earned L2-L3.

## Adopt (existing hand-built org)

For a repo that already has a CEO skill and agents (e.g. `.claude/ceo/backlog.md`,
`.claude/agents/<slug>-*.md`): **preserve content, add structure.** Never delete or rewrite an
existing agent's domain knowledge, backlog, learnings, or reports.
1. Inventory what exists and map it onto the layout above (backlog, learnings, reports, PAUSE,
   ownership map, modes).
2. Generate only what's missing: `org.json` (derived from the existing skill and agents; ask the
   feedback opt-in question as in Phase 4), `upstream.md`,
   `AUTONOMY.md`, `PRINCIPLES.md`, `memory/scorecard.md` (backfilled from `gh pr list` of past CEO
   PRs if possible), the guard hook (merged alongside any existing hooks, never replacing them),
   and seed evals.
3. For the CEO skill and each agent, produce a **gap report**: principles the existing file lacks
   (e.g. no failure-scenario bar, no freeze-the-tree rule, no autonomy gating). Propose each gap
   as a small, separate edit, and apply only the ones the user accepts.
4. The starting autonomy level for an adopted org can be backfilled from its real PR history
   using the promotion criteria. State the evidence.
5. **Don't break existing workflows.** Read every existing hook, and grep the existing skills for
   commands the guard blocks (`gh pr merge`, `git push`, `git stash`, `--no-verify`). Where an
   existing hook already does a guard job (a gate-config edit guard, a Stop-hook typecheck), keep
   it, set the matching `org.json` option off (`gate_files: []` or `guard.stop_check.cmd: ""`), and
   register only the guard modes that add something. Never run two hooks that do the same job.
   The `bash` and `edit` modes are always registered: `edit` also guards the org's control files
   (`org.json`, `AUTONOMY.md`, `settings.json`, `.claude/hooks/`), which no existing hook covers.
6. **Respect the project's own style rules** in everything you write into it (e.g. a "no em
   dashes" rule applies to copied `PRINCIPLES.md` too).

## Upgrade (re-sync with newer templates)

Read `org.json` → `agent_org_version`. For each generated file, diff the current file against
what the OLD template would have produced and against the NEW template. Keep the project's own
edits; apply only the template changes. Show the user the template-side diff before writing.
Bump `agent_org_version`. Never touch backlog, memory, learnings, reports, or evals content.

## Never

Push, open PRs, or create GitHub repos without asking. Overwrite an existing CLAUDE.md, settings
file, agent, or skill. Start above the autonomy level the verification bar supports. Generate an
agent whose perimeter globs match no files. Leave a `{{` placeholder in a generated file.
