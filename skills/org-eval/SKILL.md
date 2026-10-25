---
name: org-eval
description: Evaluate an agent org's agents and skills like unit tests. Runs each agent on known-answer cases (many mined from real fix commits in git history) inside an isolated git worktree, then scores the result with a different model as judge. Invoke as /org-eval (all cases), /org-eval <agent-name> (one agent), /org-eval mine (mine new cases from git history), or /org-eval add <agent-name> (write a case from an observed failure). Use after editing any agent definition, when the codebase has moved a lot, or before proposing an autonomy promotion.
---

# org-eval: test the org's agents

Agents degrade silently as the code moves under them and as their definitions are edited. This
skill is their test suite. Cases live in `.claude/ceo/evals/cases/*.md`; results append to
`.claude/ceo/evals/results.md`. Requires an org generated or adopted by `/org-init`
(`.claude/ceo/org.json`).

## Case format

```
---
id: <slug>-<n>
agent: <agent name in .claude/agents/>
kind: find-the-bug | fix-the-bug | gate | navigate
base: <commit sha the worktree is checked out at>
---
## Task
What the agent is told. Neutral: it must not hint at the answer.
## Expected
What a correct answer contains: the file and mechanism of the defect, a test that must pass
after the fix, the gate verdict, or the screen/file an agent should land on.
## Rubric
3-5 criteria scored 0 (missed) / 1 (partial) / 2 (met). Always include "no fabricated
file:line references" and "followed the report contract".
```

Kinds:
- **find-the-bug**: `base` = parent of a real fix commit. Agent: a hunter, reviewer, or
  specialist told to audit the module. Expected: the defect the fix addressed.
- **fix-the-bug**: same base, the agent is an editor told the symptom. Expected: the real fix's
  test (or an equivalent one) passes and no gate regresses.
- **gate**: release manager on a commit known to fail (or pass) a gate. Expected: the verdict and
  the failing gate.
- **navigate**: app-explorer or editor handed a vague report ("the share button does nothing").
  Expected: lands on the right screen and source file (tests the feature map).

## Run (`/org-eval [agent]`)

1. Read `org.json` (models, base branch) and select cases (all, or those for the named agent).
2. For each case, in parallel where cases are independent (≤4 at a time; gate cases serially,
   because they bind ports):
   a. `git worktree add --detach <scratchpad>/eval-<id> <base>`. Never use checkout or stash in
      the main tree. Link or install dependencies as the project needs.
   b. Dispatch the case's agent (`subagent_type` = the agent name) with the Task text, the
      worktree path as the repo root, and the usual brief contents (Active lessons, report
      contract). It must not see Expected or Rubric.
   c. Dispatch a **judge** with a different model from the agent's (if the agent ran on the mid
      model, judge with the top model, and vice versa), giving it Task, Expected, Rubric, and the
      agent's full report. For fix cases, the judge also gets the worktree diff and the output of
      the expected test, which you run. The judge returns per-criterion scores with a one-line
      reason each, and checks every `file:line` the agent cited actually exists.
   d. Remove the worktree.
3. Score = total / max. **Pass ≥ 0.8.** Append to `results.md`:
   `| date | case | agent | agent model | judge model | score | pass | agent def sha | note |`
   (`agent def sha` = `git hash-object .claude/agents/<agent>.md`, so a score is tied to the
   definition that earned it).
4. Report per agent: pass rate, change versus its previous run, and the failing criteria. An agent
   below 60% is **benched** (the CEO treats it as report-only) until its definition is fixed and
   re-evaluated. Say so plainly.

## Mine (`/org-eval mine`)

From `git log --since=<last mine or 6 months> -i --grep='fix\|bug\|regress' --name-only`, pick
up to 10 fixes that touched product code and came with a test. For each, draft a find-the-bug
case (and a fix-the-bug case when the fix's test is self-contained), assign the owning agent via
the ownership map, and show the drafts. Write only the ones the user accepts. Skip fixes whose
commit message gives away the answer verbatim in a way the Task can't avoid.

## Add (`/org-eval add <agent>`)

Turn an observed failure (an agent fabricated a path, grepped the wrong module, missed a bug a
lens later found) into a case that would have caught it. This is how skills improve: from real
failure modes, not imagined ones.

## Rules

- Never modify product code in the main tree. All work happens in throwaway worktrees.
- A judge never sees which agent definition version produced the report.
- Evals cost tokens: state the case count and rough cost before running more than 10 cases.
