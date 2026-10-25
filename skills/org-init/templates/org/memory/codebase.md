# {{PROJECT}}: verified facts

Read by every agent at boot. One dated bullet per fact, with evidence:
`- YYYY-MM-DD (<run or PR>): claim. file:line`
Delete a fact the moment it's falsified: a stale fact is worse than none. Keep this file around
~120 lines; merge duplicates and drop the least load-bearing. Facts that hold across many runs
and that agents keep needing get promoted into CLAUDE.md (human-approved).

## Baseline (from /org-init, {{DATE}})
{{BASELINE_FACTS}}

## Clean audits (so discovery skips these grounds)
