# Placeholder glossary

Every `{{NAME}}` in `templates/` and how to fill it. "From discovery" means from the Phase 1
reports, verified. Never fill with generic filler: if there's nothing project-specific to say,
cut the surrounding line.

## Identity and policy
| Placeholder | Fill with |
|---|---|
| `PROJECT` | display name ("MCPpedia") |
| `SLUG` | short lowercase id used in agent and skill names ("mcppedia", "maya") |
| `DATE` | today, YYYY-MM-DD |
| `AGENT_ORG_VERSION` | the `version` in this plugin's `.claude-plugin/plugin.json` |
| `ORG_SIZE` | small / standard / full |
| `PROJECT_KIND` | web-app / mobile-app / desktop-app / service / library / cli / prompt-product (comma-separate if several) |
| `AGENT_COUNT` | number of generated agents |
| `BASE_BRANCH` | usually `main` |
| `BRANCH_PREFIX` | `org/` unless the project already uses a prefix for bot branches (`ceo/`, `improve/`) |
| `AUTONOMY_LEVEL` / `AUTONOMY_TARGET` | from Phase 2 and the interview (see autonomy.md) |
| `MODEL_TOP` / `MODEL_MID` / `MODEL_SMALL` | `opus` / `sonnet` / `haiku` unless the user said otherwise |
| `MODEL_CRITIC` | `MODEL_TOP` for design/AI-quality critics (taste is judgment), else `MODEL_MID` |
| `NORTH_STAR` | one sentence: what the project must do for whom (interview) |
| `PRIORITY_ORDER` | e.g. "Correct > Fast > Beautiful" or "Stable > Lean > AI-maintainable" |
| `DEFINITION_OF_DONE` | what "works" means beyond green gates, e.g. "works on desktop (1280) AND mobile (375)"; "runs under strict CSP and SSR"; "`npm test` green and the CLI's `--help` example runs" |

## Verification
| Placeholder | Fill with |
|---|---|
| `GATES_TABLE` | markdown table `\| # \| Gate \| Command \| When \|`: real commands only, in fail-fast order (static → unit → build → e2e), plus a final "Feature check: supplied by the CEO's brief" row |
| `GATES_INLINE` | the same, inline: "`npx tsc --noEmit` ∧ `npm run lint` ∧ `npm test`" |
| `CHEAP_GATES` | the static gates that are safe to run in parallel worktrees (no ports, no shared caches) |
| `HEADLESS_GATE_TOOLS` | `Bash(<cmd>:*)` entries for each gate command, comma-separated; split compound commands (`cd dashboard && go vet ./...` → `Bash(cd dashboard:*),Bash(go vet:*)`), and include the install command |

## Team and routing
| Placeholder | Fill with |
|---|---|
| `TEAM_ROWS` | one table row per agent: `` \| `<name>` \| editor/report-only \| <perimeter or lens> \| <tier> \| `` |
| `OWNERSHIP_MAP` | bullet list `globs → agent`, most specific first, with exceptions inline (Pasa style: "`src/services/**` → qa **except** `retry\|offline*` → reliability") |
| `DEFAULT_OWNER` | the editor closest to "everything else" (often backend, or the core engineer for a library) |
| `DEPENDENCY_ORDER_HINT` | e.g. "backend first, then the UI that calls it" |
| `QUALITY_BARS` | optional `## Quality bars` section naming installed skills the org leans on and who loads them (e.g. "`taste-skill` is the design bar: the design critic grades against it. `ponytail` is the code bar: every editor loads it before writing; you run `/ponytail-review` on the full diff before the final gate"). Empty string if none installed |
| `ASSESS_ROSTER` | which agents run in each mode's assess step. Defaults: **audit/light** = security-engineer + release-manager (+ silent-failure-hunter when the run touches write paths); **deep** = every report-only specialist + critics + `<slug>-reviewer` pointed at each editor's perimeter (correctness lens). Never dispatch editors to assess: they have write tools, and "read-only mode" in a brief is not enforcement |
| `REVIEW_ROSTER` | small: "one `<slug>-reviewer` on the correctness lens (or the built-in code-review if no reviewer agent)"; standard/full: "`<slug>-reviewer` once per lens: correctness, security, regression, silent-failure (+ performance when hot paths changed)" |
| `HARD_ITEM_PIPELINE` | small/standard: "dispatch the built-in `Plan` agent at `MODEL_TOP` (read-only) for a plan, check each acceptance criterion maps to a step and a verification, then hand the plan verbatim to the owning editor at `MODEL_MID`." full: "`<slug>-researcher` (fan out one per area for large items) → `<slug>-architect` → check the plan against the acceptance criteria → owning editor with the plan verbatim." |
| `OBJECTIVE_FUNCTION` | the numbered list from roster.md with this project's nouns: name the core journeys at rank 4, the real perf budget at rank 7 |
| `NEVER_LIST` | defaults: never `--admin` merge; never force-push or push to the base branch; never deploy or run a migration against production; never point tests or walks at production; never act outward-facing (comment, close, label third-party issues/PRs) in the maintainer's name; never add a dependency without flagging it; never edit `CLAUDE.md` rules (propose them). Add project-specific items from the risk surface |

## Modes
| Placeholder | Fill with |
|---|---|
| `MODE_LIST_EXTRA` | ", /<slug>-ceo discover, ..." for each optional mode chosen |
| `MODE_ROWS_EXTRA` | one modes-table row per optional mode, four columns `\| mode \| does \| edits? \| min level \|` (discover/rnd/issues: L0, records-only; `discover fix`: L3; e2e: L1) |
| `MODE_README_ROWS` | the same rows for `.claude/ceo/README.md` |
| `EXTRA_MODES` | the chosen `templates/ceo/modes/*.md`, concatenated |
| `SCHEDULE_NOTES` | at ≥L2 target: how to run `.claude/ceo/schedule/run-headless.sh` from launchd/cron or a Claude Code routine; otherwise "Scheduling unlocks at L2 (see AUTONOMY.md)" |

## Agent bodies
| Placeholder | Fill with |
|---|---|
| `ROLE` / `ROLE_TITLE` | `frontend-engineer` / "frontend engineer" |
| `PERIMETER_SUMMARY` / `PERIMETER_GLOBS_SHORT` / `PERIMETER_TABLE` | from the ownership map; the table lists globs and what lives there |
| `NEIGHBOR_PERIMETERS` | the other editors and what they own, one line |
| `PROTECTED_PATHS_SHORT` / `PROTECTED_PATHS_LIST` | from the risk surface; always CLAUDE.md/AGENTS.md, CI workflows, `.env*`, the auth layer, migrations, gate configs, test assertions where tests are the bar |
| `USER_DATA_PATHS` | end-user data paths from discovery (also `org.json` → `user_data_paths`); "none" if the project holds no end-user data |
| `BOOTSTRAP_FRICTION` | anything in this bootstrap that was hard or ambiguous; "none" if it was smooth |
| `PROTECTED_RULE` | below L3: "the human merges it"; at L3+: "it never self-merges, even when green" |
| `CONVENTIONS` | 3-8 bullets from discovery report 4 |
| `CRITICAL_RULES` | the project's must-never-break rules, each with its reason (e.g. "the rate limiter fails OPEN by design; don't 'fix' it without a human decision") |
| `SECURITY_SURFACE` | from discovery report 3, as `file:line` pointers |
| `SILENT_FAILURE_GROUNDS` | write paths, external clients, jobs, migration scripts, as globs |
| `HUNTING_GROUNDS` | 5-10 grounds × most promising lens |
| `RND_DIRECTIONS` | the four directions with this project's ecosystem and competitors named |
| `CRITIC_*` | domain (design/motion/a11y/AI quality), subject, bar (skills to load + comparison set), failure mode ("looks like a library default"), method (how to observe it for real), extra tools (", Skill" when it loads a skill) |
| `EXPLORER_SURFACE` / `EXPLORER_HOWTO` / `CORE_JOURNEYS` / `RUN_HOWTO` | the driver (browser pane / Playwright / iOS simulator), dev command and pinned port, seed account source, viewports, journeys |
| `FEATURE_ROWS` | initial rows from routes/screens found in discovery; the explorer fills in selectors over time |

## Verify skill and repro agent
| Placeholder | Fill with |
|---|---|
| `VERIFY_DRIVERS_SHORT` | e.g. "browser pane + Playwright", "iOS simulator", "CLI invocations", "test suite + examples" |
| `VERIFY_SETUP` | exact install/seed steps in a fresh worktree (and how to link deps from the main tree when that's safe) |
| `VERIFY_START` | the start command, the pinned port, and how to confirm the process is this checkout |
| `VERIFY_DRIVE` | how to exercise each core journey: browser steps with selectors, simulator taps, CLI commands with fixture inputs, API calls |
| `VERIFY_INSPECT` | the runtime-inspection tools available and the exact commands: console/network logs, CPU traces (`--cpu-prof`, DevTools Performance), heap snapshots, profilers (pprof, Instruments), log files. Name what's NOT available |
| `VERIFY_EVIDENCE` | what to attach per claim type: output tail, screenshots per viewport, trace file paths, before/after numbers |
| `VERIFY_TEARDOWN` | stop servers, free ports, remove the worktree |
| `REPRO_EXTRA_TOOLS` | extra tools the repro agent needs to drive the app (e.g. ", mcp__playwright__*" or the browser pane tools); empty if Bash is enough |

## State seeds
| Placeholder | Fill with |
|---|---|
| `SEED_ITEMS` | backlog rows from the constraint audit and bar check, max ~8, missing gates first |
| `SEED_LESSONS` | 0-3 project-specific gotchas discovery surfaced (framework breaking changes, a port collision, a must-read doc) |
| `BASELINE_FACTS` | the Phase 2 gate results with counts and the sha they ran on |
