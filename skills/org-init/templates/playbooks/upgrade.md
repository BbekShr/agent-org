# Upgrade

## Method
1. **Read the upstream changelog and migration guide** for every version you cross, and list the
   breaking changes that touch this repo (grep for each API).
2. **One dependency (or one coupled group) per PR.** Never batch unrelated upgrades.
3. **Upgrade, then fix what broke**, applying the migration guide literally. No opportunistic
   rewrites.
4. **Full bar plus a real run** with `/{{SLUG}}-verify`. Tooling and runtime upgrades break things
   no unit test covers.
5. Lockfile committed. Note the rollback (the previous version) in the PR body.

## In this project
<!-- FILL: the package manager and lockfile, the dependencies with known breaking-change history
     (and their local docs, e.g. node_modules/<pkg>/docs), the CI toolchain versions that must match. -->
