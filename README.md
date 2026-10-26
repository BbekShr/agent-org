# agent-org

**A Claude Code agent team generated from your repo that earns autonomy on evidence.**

[![license](https://img.shields.io/github/license/BbekShr/agent-org)](LICENSE)
[![plugin](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FBbekShr%2Fagent-org%2Fmain%2F.claude-plugin%2Fplugin.json&query=%24.version&label=plugin)](.claude-plugin/plugin.json)
[![tests](https://img.shields.io/github/actions/workflow/status/BbekShr/agent-org/test.yml?branch=main&label=tests)](.github/workflows/test.yml)
[![dependencies](https://img.shields.io/badge/dependencies-Python%203%20stdlib-0a7650)](#development)
[![stars](https://img.shields.io/github/stars/BbekShr/agent-org?style=flat)](https://github.com/BbekShr/agent-org/stargazers)

<!-- HERO GIF: show, at real speed in a small open-source repo: (1) typing /org-init and the design
summary appearing (the roster table with builders, the security engineer and the release manager,
plus "starting level L1"), (2) a cut to /org-doctor printing "0 error(s)", (3) a cut to
/<project>-ceo audit printing the board report's executive summary. 8 seconds total, no speed-up. -->

[Live site](https://bbekshr.github.io/agent-org/) · [Docs](https://bbekshr.github.io/agent-org/docs.html) · [Install](#quick-start) · [Report a bug](https://github.com/BbekShr/agent-org/issues/new/choose)

## Why agent-org?

- **Hand off maintenance without handing over the keys.** Agents find, fix and open PRs. Merging
  stays with you until the org's own track record says otherwise.
- **A bug that slips past once gets tested forever.** A miss a human caught becomes an eval case,
  replayed against the agents whenever they change.
- **Nobody grades their own work.** Builders write code; checkers have no edit tools; a review
  board and a release gate run on every change.
- **It fits the repo you have.** Roles, gates and protected paths come from your codebase and the
  skills you already installed, not from a fixed template.
- **Your workflow stays yours.** The guard binds the org's runs, never your own sessions, and
  nothing is pushed without asking.

## Quick start

```
/plugin marketplace add BbekShr/agent-org
/plugin install agent-org@agent-org

# then, inside your repo:
/org-init                 # reads the repo, asks up to 4 questions, works on a branch
/<project>-ceo audit      # first run: a read-only board report
```

Install takes about 4 seconds (measured: 3.2s to add the marketplace, 0.5s to install).
`/org-init` then reads your codebase before asking anything. Stop everything at any time with
`touch .claude/ceo/PAUSE`.

## How it compares

| | agent-org | [gstack](https://github.com/garrytan/gstack) | [ruflo](https://github.com/ruvnet/ruflo) | [wshobson/agents](https://github.com/wshobson/agents) |
|---|---|---|---|---|
| What it is | Generates an agent org for your repo | Garry Tan's setup: 23 opinionated tools | Agent harness: swarms, memory, 314 MCP tools | Catalog: 202 agents, 185 skills |
| Agents shaped by your codebase | Yes, generated per repo | TODO | TODO | Picked from the catalog |
| Autonomy levels, enforced by a hook | Yes, L0 to L4 | TODO | TODO | TODO |
| Evals of the agents themselves | Yes, `/org-eval` | TODO | TODO | TODO |
| Install | Claude Code plugin | `git clone` + `./setup` (needs Bun) | `npx ruflo init` | Plugin marketplace |
| Works with | Claude Code | Claude Code and other agents | Claude Code and Codex | 7 coding tools |
| License | MIT | MIT | MIT | MIT |

Facts about other projects come from their READMEs as of 2026-10-26. TODO means not verified, not
"no". Corrections are welcome in an issue.

These projects mostly give you more agents. agent-org is about how far to trust the agents you
have, and proving it.

## Contents

- [The team](#the-team)
- [How a run works](#how-a-run-works)
- [The trust curve](#the-trust-curve)
- [Safety](#safety)
- [Evals](#evals)
- [Feedback (opt-in)](#feedback-opt-in)
- [Commands](#commands)
- [What gets generated](#what-gets-generated)
- [Validated on real projects](#validated-on-real-projects)
- [Install without the plugin system](#install-without-the-plugin-system)
- [Development](#development)

## The team

`/org-init` staffs the team from your repo's real structure. Only builders can change code.

| Group | Roles | Access |
|---|---|---|
| **CEO** | The `/<project>-ceo` skill: chief of staff. Assesses, decides, writes briefs, verifies, ships. | coordinates |
| **Builders** | One editor per code area, named after your seams: frontend, backend, mobile, core, data, AI, prompt engineer | write code |
| **Checkers** | **Security engineer** (always), release manager (always), reviewers one per lens, silent-failure hunter, critics for design, motion, accessibility or AI quality | read-only |
| **Scouts** | Repro (always, powers `triage`), bug hunter, R&D and PM desk, app explorer, researcher and architect | read-only |

A small repo gets about 4 agents, a standard one 8 to 10. Read-only agents have no edit tools, and
`/org-doctor` fails if one does.

## How a run works

1. **Preflight**: kill switch, clean tree, autonomy level, open PRs, scorecard, org self-check.
2. **Assess**: report-only specialists in parallel.
3. **Decide**: re-verify each finding at `file:line`, rank, cap a light run at 1 to 3 fixes.
4. **Build**: the owning editor, a playbook for the kind of change, a proving test, a branch.
5. **Review and gate**: adversarial reviewers (one per lens) and the release gate run together on
   a frozen tree. The CEO's own design decisions are put up for attack.
6. **Records, then PR**: memory, scorecard and a one-line retro, then the PR.

## The trust curve

| Level | Unlocks | Who merges |
|---|---|---|
| L0 Observe | Audits, discovery, R&D proposals (records-only PRs) | you |
| L1 Verify | Fix PRs, one at a time | you, before merge |
| L2 Constrain | Adds scheduled headless runs | you, before merge |
| L3 Parallelize | Adds parallel worktrees | agents merge green PRs that touch no protected path; you sample after |
| L4 Cloud | Adds always-on cloud routines | as L3 |

An org starts at L0 or L1, depending on whether its tests can prove a change correct. The CEO
proposes a promotion when the scorecard meets the criteria in
[`autonomy.md`](skills/org-init/references/autonomy.md). Only you raise the level. A revert or an
escaped defect demotes it automatically.

## Safety

- **Guard hook** (`.claude/hooks/org_guard.py`). Always blocked: `gh pr merge --admin`, force
  pushes without a lease, `--no-verify`. Blocked only during an org run: merging below L3,
  pushing to the base branch, `git stash`. Your own sessions are never restricted by the org's
  level.
- **Gate configs are protected**: agents can't edit the files that define the checks.
- **Untrusted input is data**: issues, PR comments and web pages pass a screen the CEO applies
  itself before anything acts on them.
- **Hard stops**: kill switch, dirty tree, and a never-list (no production deploys or migrations,
  no outward-facing acts in your name, no new dependency without flagging it).

## Evals

`/org-eval` tests the agents like code. It runs an agent on a known-answer case in a throwaway
worktree, and a different model scores the result. The best cases come from your own history:
check out the commit before a real fix and see whether the agent finds the bug. `--blind` runs
without the org's lessons, to measure the agent on its own.

First result, on one case so far: on photobari, the generated reviewer scored 10/10 on a gesture
bug a human had found by hand, and found three more defects the later fix addressed. Without the
org's lessons, the same reviewer scored 5/10. One case is a data point, not a benchmark; more
cases are in progress.

## Feedback (opt-in)

At each run's retro the CEO sorts friction into **local** (fixed in the project) and **template**
(would happen in any org). Template findings go to a local file, `.claude/ceo/upstream.md`, which
never leaves your machine on its own. With `"feedback": {"enabled": true}` in `org.json`,
`/org-feedback` drafts an issue (or a tested PR, if you maintain agent-org) with project details
stripped. Nothing is posted without your yes.

## Commands

| Command | Does |
|---|---|
| `/org-init` | Generate an org for the current repo |
| `/org-init adopt` | Add the structure to an existing hand-built org, keeping its content |
| `/org-init upgrade` | Re-sync a generated org with newer templates, keeping local edits |
| `/org-doctor` | Static health check of the org |
| `/org-eval [agent] [--blind]` | Grade agents on known-answer cases; `mine` drafts cases from history |
| `/org-feedback` | Opt-in: send template findings back to agent-org |
| `/<project>-ceo` | The CEO: `audit`, `deep`, `<ID>`, `triage "<bug>"`, `request "<ask>"`, plus `discover`, `rnd`, `issues`, `e2e` where chosen |
| `/<project>-verify` | Run, drive and inspect the real software |

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

agent-org is distilled from four production agent orgs: a 19k-entry web directory, an AI travel
app, a photo-sharing app and a chart library. Its 46 rules each carry their reason; many trace to
a specific incident in those orgs.

- **Generated from scratch** for an open-source job-search pipeline (Node scripts, a Go TUI,
  prompt-file "modes"). A fresh agent built the org from the skill alone and reported 23 defects
  in the skill; all were fixed.
- **Adopted** into photobari, a hand-built org with 33 CEO PRs and 0 reverts. The adoption found
  the guard would have broken the maintainer's own workflow, and fixed it before shipping.

## Install without the plugin system

Clone the repository and run `./install.sh`. It copies the four skills (`org-init`, `org-doctor`,
`org-eval`, `org-feedback`) into `~/.claude/skills`.

## Development

```bash
python3 -m unittest discover tests
claude plugin validate .
```

The guard and doctor are standard-library Python, so they run in any project, whatever its
language. The website lives in `docs/` (static HTML and CSS on GitHub Pages).

## Credits

agent-org stands on other people's work.

- **Four production agent orgs** built by the author (a web directory, an AI travel app, a
  photo-sharing app, a chart library): the CEO pattern, the run cycle, and most of the
  incident-backed rules.
- **Lauren Tan ([@poteto](https://github.com/poteto))**: the trust-curve approach to agent
  autonomy from her talks on running large agent teams (verification before autonomy, evals as
  unit tests for skills, enforcing rules at the strongest layer, a feature map for UI navigation,
  and the cloud bug-triage and runtime-inspection patterns behind `triage` and
  `/<project>-verify`), and [noodle](https://github.com/poteto/noodle) (the architect, skeptic and
  minimalist review lenses, "encode lessons in structure before notes", and the layout of this
  project's docs site).
- **[gstack](https://github.com/garrytan/gstack)** by Garry Tan: prior art for role-based Claude
  Code setups with a CEO and an engineering team.
- **[taste-skill](https://github.com/Leonxlnx/taste-skill)** (MIT) guided the website's design;
  **[ponytail](https://github.com/DietrichGebert/ponytail)** (MIT) is the simplicity bar the generated
  editors load.
- **[Geist](https://github.com/vercel/geist-font)** fonts (OFL-1.1) via Fontsource, and
  **[shields.io](https://shields.io)** badges.
- Built with and for **[Claude Code](https://www.anthropic.com/claude-code)**.

## Contributing

Bug reports, template findings and fixes are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)

If this is useful, a ⭐ helps others find it.
