## `discover` mode (hunt and FILE new bugs; never fix in the same diff)

1. Pick 3-6 hunting grounds the backlog doesn't cover. Skip grounds recorded as audited clean in
   `.claude/ceo/memory/codebase.md` within the last ~30 days.
2. Fan out `{{SLUG}}-bug-hunter` agents, one per ground × lens, in ONE message.
3. Dedupe the findings (against each other and the backlog), then re-verify the survivors
   yourself at file:line. Drop anything without a real failure scenario.
4. File the CONFIRMED findings as backlog items (failure scenario + the hunter's drafted
   acceptance criteria) and record clean audits as facts, in a **records-only PR**. Finding and
   fixing never share a diff. Stop.

`discover fix`: after the records-only PR is open, run `<ID>` on each filed item as its own PR
off `{{BASE_BRANCH}}` (worktrees if the files are disjoint). The bright line is still separate diffs.
