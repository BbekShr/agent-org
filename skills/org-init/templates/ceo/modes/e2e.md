## `e2e` mode (live app: find → fix → re-drive → ship)

Other modes assess code; `e2e` assesses the running app. Local and on-demand only.
1. **Preflight +:** the app is running (or startable) on its pinned port, and the process on that
   port is THIS repo. Not runnable → stop and report. Don't silently degrade to `audit`.
   Never point an e2e suite or walk at production.
2. **Explore:** dispatch `{{SLUG}}-app-explorer` with the prior ledger, the last "Next run should"
   list, and the core journeys.
3. **Decide:** merge ledger findings into the objective function (a broken core journey is rank 4).
   **WIP limit:** with more than ~20 open ledger rows, no new walk. Spend the run draining rows.
4. **Build → Review ∥ QA** as in the normal cycle.
5. **Re-drive:** every fix is proven on screen at each required viewport before it ships, not just
   by tests. Attach the before/after evidence to the PR.
