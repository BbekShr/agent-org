# agent-org

**Give any repo a CEO and a team of specialist agents that earn their autonomy.**

`agent-org` is a Claude Code plugin. Run `/org-init` in a project and it scans the codebase,
asks you up to four questions, and generates an org tailored to that project:

- **Specialist agents** in `.claude/agents/`: editors that own real perimeters of *your* code
  (frontend, backend, core, data, ...) plus report-only specialists (security, release gate,
  silent-failure hunter, adversarial reviewers, design/motion critics where they fit).
- **A CEO skill**, `/<project>-ceo`, the chief of staff. It assesses, delegates, verifies through
  a review board and a release gate, ships behind a PR, and writes a board report. It also takes
  plain-language requests from non-engineers (`request`) and reproduces bug reports before
  anyone fixes them (`triage`).
- **A verify skill**, `/<project>-verify`, the org's runtime eyes and hands: how to set up,
  start, drive, and inspect (traces, profiles, snapshots, screenshots) the real software, so
  agents prove their own changes instead of you acting as the go-between.
- **Org memory** in `.claude/ceo/`: one backlog, verified facts, per-agent learnings, retros,
  and a scorecard of every PR's fate.
- **Guard hooks** that make the dangerous shortcuts impossible rather than discouraged.
- **Evals** for the agents themselves, mined from your own git history.

It is distilled from five production orgs (a 19k-entry web directory, an AI travel app, a
photo-sharing app, a chart library, and their predecessors). Every rule it generates comes from
an incident that made it necessary. See [`principles.md`](skills/org-init/references/principles.md).

## The core idea

> Autonomy comes from **verification + constraints + evals + orchestration**, not from better
> prompts. Start constrained and local, prove correctness, then scale the team.

So every org climbs a **trust curve**, with each level unlocked by measured evidence:

| Level | Unlocks | Who merges |
|---|---|---|
| L0 Observe | audits, bug discovery, R&D proposals (records-only PRs) | you |
| L1 Verify | fix PRs, one at a time | you, before merge |
| L2 Constrain | + scheduled headless runs | you, before merge |
| L3 Parallelize | + parallel worktrees | agents merge green-gated PRs; you sample afterwards |
| L4 Cloud | + always-on cloud routines | as L3 |

An org starts at L0 or L1, depending on whether the project's tests and checks can actually
prove a change correct. The CEO proposes a promotion when the scorecard meets the criteria in
[`autonomy.md`](skills/org-init/references/autonomy.md), and **only you raise the level**. A
revert or escaped defect demotes the org automatically. The guard hook enforces this
mechanically during org runs: below L3, `gh pr merge` is blocked for the CEO and its agents (your own sessions are never restricted).

## Install

As a plugin (recommended):

```
/plugin marketplace add BbekShr/agent-org
/plugin install agent-org@agent-org
```

Or copy the skills into your user skills directory:

```bash
./install.sh
```

## Use

| Command | Does |
|---|---|
| `/org-init` | generate an org for the current repo (on a branch, nothing pushed without asking) |
| `/org-init adopt` | add structure (org.json, autonomy, scorecard, guard, evals) to an existing hand-built CEO/agents setup without losing its content |
| `/org-init upgrade` | re-sync a generated org with newer templates, keeping local edits |
| `/org-doctor` | static health check: dead refs, report-only agents with write tools, perimeters that match nothing, unfilled placeholders, memory budgets, guard wiring |
| `/org-eval [agent]` | run agents on known-answer cases in throwaway worktrees and grade them with a different model; `/org-eval mine` drafts cases from past fix commits |
| `/<project>-ceo [audit\|deep\|<ID>\|discover\|rnd\|issues\|e2e]` | the generated CEO |
| `/<project>-ceo request "add CSV export to the tracker"` | anyone describes a change → spec with acceptance criteria → PR |
| `/<project>-ceo triage "<bug report>"` | reproduce on current main → already fixed in `<sha>` / file it / fix it |
| `/<project>-verify` | run and inspect the real software (agents load it; so can you) |

Stop everything in a project: `touch .claude/ceo/PAUSE`.

## What gets generated

```
CLAUDE.md                         + a 4-line pointer (skipped if CLAUDE.md ships to end users)
.claude/
  agents/<slug>-*.md              the team
  skills/<slug>-ceo/SKILL.md      the orchestrator (the project's own file; the CEO maintains it)
  skills/<slug>-verify/SKILL.md   runtime eyes and hands: setup, start, drive, inspect, evidence
  hooks/org_guard.py              blocks --admin merges, force/base pushes, --no-verify,
                                  git stash, gate-config edits; Stop-hook cheap check
  settings.json                   hooks merged in (existing settings preserved)
  ceo/
    org.json                      roster, gates, protected + user-data paths, autonomy level
    RULES.md                      the org's rules (kept out of CLAUDE.md)
    backlog.md                    the one tracker
    memory/{codebase,retros,scorecard}.md
    learnings/_shared.md          only "## Active" enters agent briefs
    feature-map.md                routes, elements, selectors, files (UI projects)
    evals/cases/                  known-answer cases
    PRINCIPLES.md  AUTONOMY.md    the rules, and the trust curve
    bin/org_doctor.py             vendored so headless/cloud runs are self-contained
```

## Validated on a real project

v0.1 was dogfooded end to end on an open-source AI job-search pipeline (Node scripts, a Go TUI,
and prompt-markdown "modes"). A separate agent that hadn't seen the skill before generated the
org from it, then reported 23 defects in the skill, from "the org would have shipped to every end
user via the project's self-updater" to "eval agents would stop at boot on old commits". All 23
are fixed in this version. The generated release manager, running on the small model, then
passed its smoke test and followed the report contract exactly.

## Development

```bash
python3 -m unittest discover tests
```

The guard and doctor are stdlib-only Python so they run in any project, whatever its language.

## License

MIT
