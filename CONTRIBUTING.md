# Contributing to agent-org

Thanks for helping. agent-org is mostly Markdown (skills, templates, references) plus two small
standard-library Python scripts (the guard and the doctor) and their tests.

## Ways to help

- **Report a bug** in the generator, the doctor, the guard, or a generated org:
  [open a bug report](https://github.com/BbekShr/agent-org/issues/new?template=bug_report.yml).
- **Send a template finding**: something your org hit that would happen in any org built from the
  same templates. `/org-feedback` drafts these for you (opt-in), or use the
  [template finding form](https://github.com/BbekShr/agent-org/issues/new?template=template_finding.yml).
- **Propose a feature**: [feature request](https://github.com/BbekShr/agent-org/issues/new?template=feature_request.yml).
- **Pick up a good first issue** (below).

Please don't include private code, file paths, data, or secrets from your own projects in issues.

## Repository layout

```
skills/
  org-init/          the generator: SKILL.md, references/ (principles, roster, autonomy,
                     skills registry, placeholder glossary), templates/ (agents, CEO, org state,
                     hooks, playbooks, verify skill, schedule)
  org-doctor/        static health check (scripts/org_doctor.py)
  org-eval/          agent evals (known-answer cases, different-model judge)
  org-feedback/      opt-in template findings back to this repo
tests/               unit tests for the guard and the doctor
docs/                the website (static HTML and CSS, GitHub Pages)
```

## Development

```bash
python3 -m unittest discover tests     # 40 tests, standard library only
claude plugin validate .               # plugin manifest
```

To try your changes in a real repo, install from your clone with `./install.sh` (it copies the
skills into `~/.claude/skills`), then run `/org-init` in a test project.

## Rules for changes

- **Keep the scripts dependency-free.** The guard and doctor run in any project, whatever its
  language; they use only the Python standard library.
- **Every behaviour change in a script ships with a test** in `tests/`.
- **Every new template placeholder** is documented in
  `skills/org-init/references/placeholders.md`.
- **A new rule in `principles.md`** carries its one-line reason. If it comes from an incident, say
  which kind.
- **No em dashes** in any file. Use a comma, a colon, or a new sentence.
- Keep agent templates short. The best agents in the source orgs are 40 to 140 lines.

## Good first issues

Real, small tasks found in the code. Each one has a clear done state.

1. **Guard: support file paths in `guard.stop_check.watch`.**
   `templates/hooks/org_guard.py` walks each `watch` entry with `os.walk`, which silently yields
   nothing for a file. Accept files as well as directories. Done when a test in
   `tests/test_org_guard.py` covers a watched file.
2. **Doctor: check references that have no slash.**
   `check_refs` in `skills/org-doctor/scripts/org_doctor.py` only matches paths containing `/`, so
   a dead reference like `` `CLAUDE.md` `` or `` `RULES.md` `` is never caught. Extend the pattern
   without flagging ordinary words. Done when a test covers a dead root-level reference.
3. **Docs: document `BOOT` and `REPORT_CONTRACT` in the placeholder glossary.**
   They are used by every agent template but missing from
   `skills/org-init/references/placeholders.md`. Explain that they are pasted from
   `templates/agents/_contract.md`.
4. **`install.sh`: add `--force` to reinstall over an existing copy.**
   Today it skips any skill that already exists in `~/.claude/skills`. Add a `--force` flag that
   replaces it, and keep the safe default.
5. **Website: add a favicon and an `og:image`.**
   `docs/index.html` and `docs/docs.html` have neither, so shared links show no preview. A simple
   1280x640 image and a small SVG favicon in `docs/assets/` are enough.

## Pull requests

Branch from `main`, keep each PR to one logical change, and describe how you verified it. Run the
tests before pushing; CI runs them on every PR.

By contributing you agree your work is licensed under the [MIT License](LICENSE).
