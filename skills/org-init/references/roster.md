# Roster catalog

Pick agents from this catalog using the signals found in discovery. Every agent file is named
`<slug>-<role>.md` and its frontmatter `name` matches the filename. The template for each lives
in `templates/agents/`.

## Always generated, at every size

`<slug>-release-manager`, `<slug>-security-engineer`, `<slug>-repro`, the CEO skill (the chief of
staff: coordination, prioritization, routing), and the `<slug>-verify` skill (the org's runtime
eyes and hands).

## Org size (choose one; it decides the default roster)

| Size | When | Default roster |
|---|---|---|
| `small` | < ~15k LOC, one main surface, ≤1 contributor, or no test suite yet | 1-2 editors, `security-engineer`, `release-manager` |
| `standard` | most projects | 2-4 editors, `security-engineer`, `release-manager`, `silent-failure-hunter`, `reviewer`, + any critics the signals call for |
| `full` | large or high-stakes codebases, many surfaces, a real backlog, external contributors | standard + `researcher`, `architect`, `bug-hunter`, `rnd` (and `issues` mode if the repo takes public issues) |

Default to the smaller size when unsure. The org can grow later via `/org-init upgrade`.

## Editors (write product code; one per perimeter)

Derive editors from the codebase's real seams, not from a generic list. An editor's perimeter is
a set of globs that is (a) cohesive, (b) large enough to matter, and (c) owned by one skill set.
Two editors minimum when the project has a clear client/server split; one when it doesn't.

Common perimeters and the signals that call for them:

| Editor role | Signals | Typical perimeter |
|---|---|---|
| `frontend-engineer` | React/Vue/Svelte/Next pages, `components/`, CSS/Tailwind | pages, components, styles, UI tests |
| `backend-engineer` | API routes, server handlers, DB clients, migrations, workers | api, lib/server, db, migrations, scripts |
| `mobile-engineer` | Expo/React Native/Swift/Kotlin app dirs | app screens, native modules, stores |
| `core-engineer` | a library: `src/` exporting a public API, no app shell | the library core and its unit tests |
| `data-engineer` | ETL, bots, cron jobs, scheduled workflows, scrapers | bots/, jobs/, pipelines, workflow scripts |
| `ai-engineer` | LLM calls, prompts, agent loops, eval harness | prompts, ai/, model boundary, evals |
| `prompt-engineer` | the product logic itself is prompt/markdown instructions an agent follows (`modes/*.md`, skill files, worker prompts), often with localized mirrors that must stay in sync | prompt files and their mirrors, command wrappers (never the root rules file: that's a protected path) |
| `infra-engineer` | Terraform, Docker, k8s, deploy config as a primary surface | infra/, deploy config (never applies to prod) |

Each editor writes the test for its own fix. Name the default owner for anything unlisted.

## Report-only specialists

| Role | Include when | Model tier |
|---|---|---|
| `security-engineer` | always | mid |
| `release-manager` | always: owns the GO/NO-GO gate and runs the verification bar verbatim | small |
| `silent-failure-hunter` | any write path, external API, queue, upload, migration, or bot | mid |
| `reviewer` | standard+: adversarial, spawned once per lens (correctness, security, regression, silent-failure, performance) | mid; top for correctness on hard diffs |
| `performance-engineer` | a perf budget exists, hot paths, bundle-size concerns, mobile | mid |
| `design-critic` | a user-facing UI where look and feel matter | top |
| `motion-critic` | meaningful animation, gestures, transitions | mid |
| `a11y-critic` | public-facing UI without a design critic (fold into design-critic otherwise) | mid |
| `ai-quality-critic` | LLM output is the product (grades output quality, never edits prompts) | top |
| `app-explorer` | a runnable app that can be driven (browser pane, Playwright, simulator) for an `e2e` mode | mid |
| `repro` | always: reproduces bug reports on current main via the verify skill (powers `triage`; always-on in the cloud at L4) | mid |

Critics grade against a named bar. If a matching skill is installed (e.g. `taste-skill` for
design, `ponytail` for simplicity, `dataviz` for charts), the critic loads it via the Skill tool
instead of working from memory. Check the installed-skills list during discovery.

## Pipeline agents (`full` size, or on demand)

| Role | Job | Access |
|---|---|---|
| `researcher` | map the blast radius of an item: touched surface, reuse inventory, risks, conventions | read-only |
| `architect` | turn item + brief into an ordered plan with a verification plan | read-only (no Bash) |
| `bug-hunter` | discovery mode: hunt NEW bugs in one ground × one lens, with drafted acceptance criteria | read-only |
| `rnd` | the PM/product desk: R&D mode proposals (features, process) with evidence and drafted specs; also drafts specs for `request` mode when the ask is large | read-only |

**Mode dependencies override size:** choosing `discover` or `issues` mode always adds
`bug-hunter`; choosing `rnd` always adds `rnd`; choosing `e2e` always adds `app-explorer`.

At `small`/`standard` size, use the built-in `Explore` agent for research and the built-in
`Plan` agent (top model) for design instead of generating these.

## Objective function (default ranking; adapt the nouns to the project)

1. Red gates (typecheck/lint/test/build failing)
2. Security / privacy (leaked secrets, auth holes, cross-user data access)
3. Crashes and data loss (unhandled rejections, partial writes, swallowed write errors)
4. Correctness bugs in the core journeys (name them: e.g. "sign up → create → share")
5. Missing tests on critical untested paths
6. Org drift (an agent misfired because its instructions were wrong; doctor errors)
7. Performance regressions
8. Polish

Swallowed errors on write paths rank at 3, not at polish: a failure nobody sees is worse than
one they do. Org drift outranks perf/polish because a broken agent degrades every later run.
