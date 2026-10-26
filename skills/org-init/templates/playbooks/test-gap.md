# Test gap

## Method
1. **Test the invariant, not the current behaviour.** A test that mirrors whatever the code does
   today is not a guard. Write what *should* be true, from the docs, the contract, or the item.
2. **Prove each test has teeth**: break the code on purpose (in your worktree only), watch the test
   fail, then restore it. A test that can't fail is decoration.
3. **Behaviour over shape.** A test against a stub that doesn't execute the behaviour (ordering,
   filtering, auth, caching) proves a call was made, not that it's right. Prefer real fixtures.
4. **Fast and deterministic**: no network, no wall-clock sleeps, no order dependence.
5. Wire the new tests into the gate that CI runs, or they don't exist.

## In this project
<!-- FILL: the test framework and layout, fixture conventions, the gate that runs tests in CI, and
     whether that gate file is protected (then wiring needs the human: ALLOW_GATE_EDITS). -->
