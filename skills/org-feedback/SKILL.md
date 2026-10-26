---
name: org-feedback
description: Opt-in feedback channel from an agent org back to agent-org itself. Turns the template findings a project's CEO runs recorded in .claude/ceo/upstream.md into a GitHub issue (a problem that needs a decision) or a pull request (a concrete, tested fix) on the agent-org repo, with project details stripped and nothing posted without the user's yes. Invoke as /org-feedback (draft from this project), /org-feedback send (post the reviewed drafts), or /org-feedback --projects <path> <path> (maintainers: collect across several projects). Requires "feedback": {"enabled": true} in .claude/ceo/org.json.
---

# org-feedback: send what your org learned back to agent-org

Every project org records **template findings** (problems that would happen in any org built
from the same agent-org templates) in `.claude/ceo/upstream.md`. That file is local and always
written. This skill is the only thing that sends any of it anywhere, and only when the user has
opted in and approves the exact text.

## Gate (stop at the first "no")

1. `.claude/ceo/org.json` → `feedback.enabled` is `true`. If not, say: "Feedback is off for this
   org. Turn it on with `\"feedback\": {\"enabled\": true}` in .claude/ceo/org.json, or leave it
   off: the outbox still records findings locally." and stop. Never turn it on yourself.
2. `.claude/ceo/upstream.md` has entries with `status: new`. If none, say so and stop.
3. `gh auth status` succeeds. If not, offer to write the drafts to a local file instead.

## Steps

1. **Read** the `status: new` entries (with `--projects`, from each listed project's outbox).
2. **Re-verify each one against the current templates** of this installed agent-org (this skill's
   sibling directories: `../org-init/templates/`, `../org-init/references/`, `../org-doctor/`).
   A finding about agent-org v0.1.0 may already be fixed in the version installed now. Mark those
   `status: fixed-upstream` with the reason and drop them.
3. **Dedupe:** findings about the same template file and mechanism become one item that lists
   how many projects or runs hit it. Repetition is evidence; keep the count.
4. **Strip project details** from everything that will leave the machine:
   - no project name, repo name, file paths outside agent-org, code, backlog or report contents,
     customer, product, or user data, secrets, internal URLs, or people's names;
   - describe the project only by kind ("a Next.js web app on Workers", "a CLI with a Go TUI");
   - quote agent-org's own files freely; paraphrase anything from the project.
   Then reread every draft looking only for leaks. When in doubt, cut it.
5. **Pick a form per item.** Check `gh repo view <upstream> --json viewerPermission`:
   - `ADMIN` / `MAINTAIN` / `WRITE` (a maintainer): a **PR** when the fix is concrete and you can
     prove it (template change plus a doctor test or a guard test that fails before and passes
     after, `python3 -m unittest discover tests` green in a clone of the upstream repo), else an
     **issue**;
   - anyone else: always an **issue**. Put the proposed change in the issue body as a suggested
     diff; never fork or push on the user's behalf.
6. **Show the drafts** (title, body, and for PRs the diff), numbered, and the target repo. Then stop
   and wait for `/org-feedback send` or a plain yes naming which drafts to send.

## Send (`/org-feedback send`, only after the user approved the drafts in this session)

- Issues: `gh issue create --repo <upstream> --title ... --body-file <draft>`. Add `--label
  org-feedback` only if that label exists (`gh label list --repo <upstream>`); a maintainer may
  create it first with `gh label create org-feedback --repo <upstream>`; anyone else sends
  unlabeled.
- PRs (maintainers only): clone the upstream into the scratchpad, branch `feedback/<slug>`, apply
  the change, run the tests, push, `gh pr create`. Never push to the upstream's default branch.
- After each send, set the outbox entry to `status: sent <url>` and commit the outbox change in the
  project with the run's other records (or on its own branch if the tree is shared).
- Report the URLs.

## Issue body template

```
**Template:** <agent-org file, e.g. skills/org-init/templates/agents/critic.md>
**agent-org version:** <from org.json agent_org_version>
**Seen in:** <N> run(s) across <M> org(s) (<project kinds>)

**What happened**
<the mechanism, in agent-org's terms>

**Why it is a template problem, not a project one**
<what in the template makes it recur in any org>

**Evidence**
<doctor output, a guard test, an eval score, with project details stripped>

**Proposed change**
<a suggested diff or a concrete description>

Sent with /org-feedback (opt-in). No project code or data is included.
```

## Never

Post anything without `feedback.enabled: true` and the user's yes to the specific drafts in this
session; send project code, paths, data or names; fork, push, or open a PR as a non-maintainer;
comment on, close, or label existing issues; batch-send drafts the user did not review.
