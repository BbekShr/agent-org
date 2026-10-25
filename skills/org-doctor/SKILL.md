---
name: org-doctor
description: Health check for an agent org created by /org-init. Statically validates org.json, every agent definition (frontmatter, report-only agents can't write, perimeter globs match real files, dead file references), the CEO skill (every agent it dispatches exists), unfilled placeholders, memory budgets, guard wiring, and eval coverage. Invoke as /org-doctor. The CEO runs it in every preflight; run it after any edit to .claude/agents, the CEO skill, or .claude/ceo.
---

# org-doctor

Run:

```bash
python3 "<this skill's directory>/scripts/org_doctor.py" "$(git rev-parse --show-toplevel)"
```

Then report the result in three groups: **errors** (must fix: each one means an agent will
misfire or a guard is off), **warnings** (drift worth fixing this run if it's cheap), and
**info**. For each error, say the one-line fix.

The script is static and cheap. It cannot see behavioural drift: an agent whose instructions
are still well formed but no longer produce good work. That is what `/org-eval` measures. If the
doctor is clean but an agent misfired in the last run, suggest `/org-eval <agent>`.

Exit codes: 0 clean (warnings allowed), 1 errors, 2 no org found (suggest `/org-init`, or
`/org-init adopt` if `.claude/agents/` already exists).

If asked to fix the findings: org files are the CEO's perimeter. Fix errors surgically (a
renamed path, a missing `tools:` line, a stale glob), re-run the doctor, and run
`/org-eval <agent>` for any agent whose definition you changed.
