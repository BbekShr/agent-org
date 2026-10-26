# agent-org

**A CEO and a team of specialist agents for any repo, with autonomy earned on evidence.**

[Website](https://bbekshr.github.io/agent-org/) · [Docs](https://bbekshr.github.io/agent-org/docs.html) · [Principles](skills/org-init/references/principles.md)

agent-org is a Claude Code plugin. Run `/org-init` in a project and it reads the codebase, asks
up to four questions, and generates an org fitted to that repo: agents that own real parts of
your code, agents that only check, a CEO skill that runs them, and the guards, memory and evals
that let the org earn more autonomy over time.

It is distilled from four production agent orgs (a 19k-entry web directory, an AI travel app, a
photo-sharing app, and a chart library). Every rule it generates exists because an incident made
it necessary.

> Autonomy comes from **verification + constraints + evals + orchestration**, not from better
> prompts. Start constrained and local, prove correctness, then scale the team.

## Contents

- [Install](#install)
- [Quick start](#quick-start)
- [The team](#the-team)
- [How a run works](#how-a-run-works)
- [The trust curve](#the-trust-curve)
- [Safety](#safety)
- [Evals](#evals)
- [Feedback (opt-in)](#feedback-opt-in)
- [Commands](#commands)
- [What gets generated](#what-gets-generated)
- [Validated on real projects](#validated-on-real-projects)
- [Development](#development)

## Install

As a plugin:

```
/plugin marketplace add BbekShr/agent-org
/plugin install agent-org@agent-org
```

Without the plugin system, clone the repo and run `./install.sh` (copies the skills into
`~/.claude/skills`).

## Quick start

```
/org-init                 # generate an org for this repo (on a branch; nothing pushed without asking)
/<project>-ceo audit      # first run: read-only board report
/<project>-ceo            # light run: fix the top 1-3 items, open a PR
touch .claude/ceo/PAUSE   # kill switch: stops every mode
```

Already have a hand-built CEO and agents? Use `/org-init adopt`: it adds the missing structure
without removing your content.

## The team

`/org-init` staffs the team from your repo's real structure. Only builders can change code;
everyone else reports.

| Group | Roles | Access |
|---|---|---|
| **CEO** | the `/<project>-ceo` skill: chief of staff, routes work, decides, ships | coordinates |
| **Builders** | one editor per code area, named after your seams: frontend, backend, mobile, data, AI, prompt engineer | write code |
| **Checkers** | **security engineer** (always), release manager (always), reviewers one per lens, silent-failure hunter, critics (design, motion, a11y, AI quality) | read-only |
| **Scouts** | repro (always, powers `triage`), bug hunter, R&D/PM desk, app explorer, researcher and architect | read-only |

A small repo gets about 4 agents, a standard one 8 to 10, a large one more. Read-only agents have
no edit tools, and `/org-doctor` enforces it.

## How a run works

1. **Preflight**: kill switch, clean tree, autonomy level, open PRs, scorecard, org self-check.
2. **Assess**: report-only specialists in parallel.
3. **Decide**: re-verify each finding at `file:line`, rank, cap a light run at 1 to 3 fixes.
4. **Build**: the owning editor, a playbook for the kind of change, a proving test, a branch.
5. **Review ∥ QA**: adversarial reviewers (one per lens) and the release gate together, on a
   frozen tree. The CEO's own design decisions are put up for attack.
6. **Records and PR**: memory, scorecard, a micro-retro, then the PR.

Each run leaves memory behind, so the next one starts smarter.

## The trust curve

| Level | Unlocks | Who merges |
|---|---|---|
| L0 Observe | audits, discovery, R&D proposals (records-only PRs) | you |
| L1 Verify | fix PRs, one at a time | you, before merge |
| L2 Constrain | + scheduled headless runs | you, before merge |
| L3 Parallelize | + parallel worktrees | agents merge green PRs; you sample after |
| L4 Cloud | + always-on cloud routines | as L3 |

An org starts at L0 or L1, depending on whether its tests can prove a change correct. The CEO
proposes a promotion when the scorecard meets the criteria in
[`autonomy.md`](skills/org-init/references/autonomy.md); **only you raise the level**. A revert
or escaped defect demotes it automatically.

## Safety

- **Guard hook** (`.claude/hooks/org_guard.py`). Always blocked: `gh pr merge --admin`,
  non-lease force pushes, `--no-verify`. Blocked only during an org run: merging below L3,
  pushing to the base branch, `git stash`. Your own sessions are never restricted by the org's
  level.
- **Gate configs are protected**: agents can't edit the files that define the checks.
- **Untrusted input is data**: issues, PR comments and web pages pass a screen the CEO applies
  itself before anything acts on them.
- **Hard stops**: kill switch, dirty tree, and a never-list (no production deploys or
  migrations, no outward-facing acts in your name, no new dependency without flagging it).

## Evals

`/org-eval` tests the agents like code. It runs an agent on known-answer cases in a throwaway
worktree and has a different model judge the result. The best cases come from your own history:
check out the commit before a real fix and see whether the agent finds the bug. `--blind` runs
without the org's lessons, to measure the agent itself.

## Feedback (opt-in)

At each micro-retro the CEO sorts friction into **local** (fixed in the project) and
**template** (would happen in any org). Template findings go to a local outbox,
`.claude/ceo/upstream.md`, which never leaves your machine on its own. With
`"feedback": {"enabled": true}` in `org.json`, `/org-feedback` turns them into drafts: an issue,
or a tested PR if you maintain agent-org. Project details are stripped, and nothing is posted
without your yes.

## Commands

| Command | Does |
|---|---|
| `/org-init` | generate an org for the current repo |
| `/org-init adopt` | add the structure to an existing hand-built org, keeping its content |
| `/org-init upgrade` | re-sync a generated org with newer templates, keeping local edits |
| `/org-doctor` | static health check of the org |
| `/org-eval [agent] [--blind]` | grade agents on known-answer cases; `mine` drafts cases from history |
| `/org-feedback` | opt-in: send template findings back to agent-org |
| `/<project>-ceo` | the generated CEO: `audit`, `deep`, `<ID>`, `triage "<bug>"`, `request "<ask>"`, plus `discover`, `rnd`, `issues`, `e2e` where chosen |
| `/<project>-verify` | run, drive and inspect the real software |

## What gets generated

```
CLAUDE.md                         + a 4-line pointer (skipped if CLAUDE.md ships to end users)
.claude/
  agents/<slug>-*.md              the team
  skills/<slug>-ceo/SKILL.md      the orchestrator (the project's own file from then on)
  skills/<slug>-verify/SKILL.md   setup, start, drive, inspect, evidence, teardown
  hooks/org_guard.py              the guard
  settings.json                   hooks merged in (existing settings kept)
  ceo/
    org.json                      roster, gates, protected and user-data paths, skills, autonomy
    RULES.md                      the rules every agent gets in its brief
    backlog.md                    the one tracker for open work
    memory/                       codebase facts, retros, scorecard
    learnings/                    lessons; only "## Active" enters briefs
    playbooks/                    bug fix, perf, feature, refactor, security, upgrade, test gap
    evals/                        known-answer cases and results
    upstream.md                   template findings for agent-org (local unless you opt in)
    PRINCIPLES.md  AUTONOMY.md    the rules with their reasons, and the trust curve
    bin/org_doctor.py             vendored so headless and cloud runs are self-contained
```

## Validated on real projects

- **Generated from scratch** for an open-source job-search pipeline (Node scripts, a Go TUI,
  prompt-file "modes"). A fresh agent built the org from the skill alone and reported 23 defects
  in the skill; all were fixed.
- **Adopted** into photobari, a hand-built org with 33 CEO PRs of history. The adoption found the
  guard would have broken the maintainer's own workflow, and fixed it. The new reviewer then
  scored **10/10** on a real bug a human had to find by hand, plus three more defects the later
  fix addressed. The same agent without the org's lessons scored 5/10.

## Development

```bash
python3 -m unittest discover tests
claude plugin validate .
```

The guard and doctor are stdlib-only Python, so they run in any project, whatever its language.
The website lives in `docs/` (static HTML and CSS, served by GitHub Pages).

## License

MIT
