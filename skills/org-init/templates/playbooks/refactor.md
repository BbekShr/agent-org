# Refactor

## Method
1. **No behaviour change, provably.** Before touching code, make sure tests pin the current
   behaviour of everything you'll move. If they don't, write those tests first, as their own
   commit.
2. **Small, mechanical steps**, each one green. Rename, move, extract, inline. Never rewrite.
3. **No new features, no bug fixes** in the same diff. Found a bug? Write it down as a `FACT:`
   line and leave it.
4. **The diff should shrink or hold steady.** A refactor that adds net lines needs a reason.
5. Gates green after every step, and the same public behaviour (outputs, API, UI) at the end.

## In this project
<!-- FILL: the target structure (e.g. collocated feature directories), the import boundaries
     that must hold, and the files that are duplicated contracts and must change together. -->
