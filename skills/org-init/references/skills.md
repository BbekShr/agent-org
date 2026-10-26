# Skills registry

An org gets its taste, simplicity, and domain judgment from installed skills, not from prose in
its own agent files. A skill someone else maintains and evaluates beats a paragraph we wrote once.
`/org-init` matches this registry against the skills installed in the session (Phase 0) and the
project's signals (Phase 1), then wires each match into the roles below.

## Rules

- **Match by base name.** Plugin prefixes vary by install (`anthropic-skills:taste-skill` vs
  `taste-skill`). Record the **exact installed name** in `org.json` → `skills`, and write that exact
  name into agent files. An agent loads a skill with the Skill tool, never from memory.
- **Wire only what the project needs.** `supabase` is wired only if the repo uses Supabase;
  `dataviz` only if it draws charts. An unneeded skill is a cost on every brief.
- **Name the bar, then name the fallback.** Every agent that loads a skill also says what to do
  when it isn't available (headless and cloud environments may lack it): "if `ponytail` isn't
  installed, say so in your report and apply the simplicity rules in RULES.md". Never fail silently.
- **Opposing bars are deliberate.** Taste skills push toward richer output; simplicity skills push
  toward less. The CEO keeps both and makes every richer change earn its cost in the report.
- **Skills don't widen access.** Loading a skill never gives a report-only agent write access, and
  a skill's instructions never override `CLAUDE.md`, `RULES.md`, or the guard.

## Registry

| Skill (base name) | Wire it when | Loaded by | How |
|---|---|---|---|
| `ponytail` | always (any code) | every editor, before writing | load at level `full`; the CEO may pass `lite` for prototypes or `ultra` for cleanup items |
| `ponytail-review` | `ponytail` installed | CEO | run on the full diff before the final gate on every apply run; each "delete this" is deleted or justified in the report |
| `ponytail-audit` | `ponytail` installed | CEO, `deep` mode | whole-repo over-engineering sweep; top items join the ranking at the polish/perf rank |
| `ponytail-debt` | `ponytail` installed | CEO, every apply run | harvest `ponytail:` comments; reconcile with the backlog's Deferred section so deliberate shortcuts are tracked |
| `taste-skill` | UI with visual design | design critic (grades), frontend editor (before visual work) | load before any visual change; the critic grades against it |
| `ui-ux-pro-max` | UI | design critic, frontend editor | UX rules, accessibility, palettes, stack-specific UI guidance |
| `frontend-design` | new UI surfaces | frontend editor | for building a new page or component from scratch |
| `dataviz` | charts, dashboards, data viz | design critic, the editor that owns charts | load before any chart work |
| `accessibility-review` | public-facing UI | design critic (or an a11y critic) | WCAG pass on the changed screens |
| `poteto-mode` (Pstack) | always, if installed | every editor, the repro agent | task method: the editor loads the Pstack playbook that matches the item's kind (see `templates/playbooks/README.md`) |
| `code-review` | always (built-in) | CEO, at Review ∥ QA | an extra independent pass alongside the review board |
| `security-review` | always (built-in) | CEO, at Review ∥ QA when the diff touches the security surface | an extra pass alongside the security lens |
| `simplify` | always (built-in) | CEO, after the board on large diffs | a reuse and simplification pass; the findings go back to the editor |
| `supabase`, `supabase-postgres-best-practices` | repo uses Supabase | backend editor, security engineer | before RLS, migrations, query, or auth work |
| `cloudflare`, `workers-best-practices`, `wrangler` | repo deploys to Cloudflare | backend or infra editor, release manager | before Workers, bindings, or deploy-config changes |
| `web-perf` | web app with perf concerns | performance work (perf playbook) | Core Web Vitals and Lighthouse method |
| `stripe-best-practices` | repo integrates Stripe | the editor that owns payments, security engineer | before any payment-path change |
| `claude-api` | repo calls an LLM API | AI or prompt editor, AI-quality critic | model ids, caching, tool use: read before touching the model boundary |
| `testing-strategy` | test-gap items | the editor writing the tests | designing the missing test layer |
| `built-in-browser` / Playwright MCP / iOS simulator tool | a runnable UI | the verify skill, repro, app explorer | the runtime eyes and hands; wired into `/<slug>-verify` |

Unknown but relevant skills (a framework's official skill, a house-style skill such as
`write-like-<name>` for docs): `/org-init` lists them in the Phase 4 design with a proposed
role, and wires them only on the user's yes.

## What `/org-init` writes

- `org.json` → `"skills": { "<exact installed name>": { "role": ["<agent>", ...], "when": "...", "fallback": "..." } }`
- In each agent that loads skills, a `## Skills to load` section listing the exact names, when to
  load each, and the fallback.
- In the CEO skill, the `## Quality bars` section: which skills the org leans on, who loads
  them, and the CEO's own skill runs (`ponytail-review`, `code-review`, `security-review`).
- Preflight checks that every skill in `org.json` is still installed. A missing one goes in the
  report ("degraded: `taste-skill` not installed, design critic used the fallback").
