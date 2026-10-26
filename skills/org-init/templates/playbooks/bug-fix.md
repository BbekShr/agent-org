# Bug fix

## Method
1. **Reproduce first** on your branch's base with `/{{SLUG}}-verify`. No repro, no fix: report
   CAN'T REPRODUCE with what you tried.
2. **Write the failing test** that captures the bug, and watch it fail for the reported reason.
3. **Find the root cause**, not the symptom: why was the wrong value possible at all? Check every
   caller of the function you're about to change.
4. **Smallest fix** that makes the test pass. No drive-by refactors.
5. **Look for siblings**: the same mistake elsewhere (grep the pattern). Fix them in scope, or list
   them as `FACT:` lines for new backlog items.
6. Re-run the repro: it must now behave correctly, with evidence.

## In this project
<!-- FILL: the test runner and where a regression test for each perimeter goes; the fixture
     data to use; known traps (e.g. "the harness runs scripts on EMPTY data, so prove script
     changes on a fixture"). -->
