"""Tests for skills/org-doctor/scripts/org_doctor.py. Run: python3 -m unittest discover tests"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
DOCTOR = os.path.join(HERE, "..", "skills", "org-doctor", "scripts", "org_doctor.py")
GUARD = os.path.join(HERE, "..", "skills", "org-init", "templates", "hooks", "org_guard.py")
SNIPPET = os.path.join(HERE, "..", "skills", "org-init", "templates", "hooks", "settings.snippet.json")


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def agent(name, tools=None, body=""):
    t = f"tools: {tools}\n" if tools else ""
    return (f"---\nname: {name}\ndescription: A sufficiently long description for routing this agent correctly.\n"
            f"{t}---\n\n# {name}\n{body}\n")


class DoctorTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        subprocess.run(["git", "init", "-q"], cwd=self.root)
        write(self.root, "src/app/page.tsx", "x")
        write(self.root, "src/api/route.ts", "x")
        write(self.root, "tsconfig.json", "{}")
        self.org = {
            "project": "Demo", "slug": "demo", "ceo_skill": "demo-ceo", "base_branch": "main",
            "autonomy_level": "L1", "autonomy_target": "L3",
            "gates": [{"name": "typecheck", "cmd": "tsc", "cheap": True}], "gate_files": ["tsconfig.json"],
            "agents": [
                {"name": "demo-frontend-engineer", "access": "editor", "perimeter": ["src/app/**"]},
                {"name": "demo-release-manager", "access": "report-only", "perimeter": []},
            ],
        }
        write(self.root, ".claude/agents/demo-frontend-engineer.md", agent("demo-frontend-engineer"))
        write(self.root, ".claude/agents/demo-release-manager.md", agent("demo-release-manager", "Bash, Read, Grep"))
        write(self.root, ".claude/skills/demo-ceo/SKILL.md",
              "---\nname: demo-ceo\ndescription: CEO\n---\nDispatch `demo-frontend-engineer` and `demo-release-manager`.\n")
        for f in ("RULES.md", "backlog.md", "memory/codebase.md", "memory/retros.md", "memory/scorecard.md", "AUTONOMY.md", "PRINCIPLES.md"):
            write(self.root, f".claude/ceo/{f}", "# x\n")
        write(self.root, ".claude/ceo/learnings/_shared.md", "## Active\n- one\n\n## Archive\n")
        write(self.root, ".claude/ceo/evals/cases/c1.md", "---\nid: demo-1\nagent: demo-frontend-engineer\n---\n")
        os.makedirs(os.path.join(self.root, ".claude", "hooks"), exist_ok=True)
        shutil.copy(GUARD, os.path.join(self.root, ".claude", "hooks", "org_guard.py"))
        shutil.copy(SNIPPET, os.path.join(self.root, ".claude", "settings.json"))
        self.save()
        subprocess.run(["git", "add", "-A"], cwd=self.root)

    def save(self):
        write(self.root, ".claude/ceo/org.json", json.dumps(self.org))

    def doctor(self):
        res = subprocess.run([sys.executable, DOCTOR, self.root, "--json"], capture_output=True, text=True)
        return res.returncode, json.loads(res.stdout) if res.stdout.startswith("{") else res.stdout

    def assertError(self, fragment):
        code, out = self.doctor()
        self.assertEqual(code, 1, out)
        self.assertTrue(any(fragment in e for e in out["errors"]), out["errors"])

    def test_clean_org(self):
        code, out = self.doctor()
        self.assertEqual(code, 0, out)
        self.assertEqual(out["errors"], [])

    def test_no_org(self):
        os.remove(os.path.join(self.root, ".claude", "ceo", "org.json"))
        code, _ = self.doctor()
        self.assertEqual(code, 2)

    def test_missing_agent_file(self):
        os.remove(os.path.join(self.root, ".claude", "agents", "demo-frontend-engineer.md"))
        self.assertError("is missing")

    def test_report_only_without_tools_inherits_write(self):
        write(self.root, ".claude/agents/demo-release-manager.md", agent("demo-release-manager"))
        self.assertError("inherits Edit/Write")

    def test_report_only_with_write_tool(self):
        write(self.root, ".claude/agents/demo-release-manager.md", agent("demo-release-manager", "Bash, Edit"))
        self.assertError("write tools")

    def test_perimeter_matches_nothing(self):
        self.org["agents"][0]["perimeter"] = ["web/**"]
        self.save()
        self.assertError("matches no tracked file")

    def test_ceo_dispatches_unknown_agent(self):
        write(self.root, ".claude/skills/demo-ceo/SKILL.md",
              "---\nname: demo-ceo\ndescription: CEO\n---\n`demo-frontend-engineer` `demo-release-manager` `demo-ghost`\n")
        self.assertError("demo-ghost")

    def test_unfilled_placeholder(self):
        write(self.root, ".claude/agents/demo-frontend-engineer.md", agent("demo-frontend-engineer", body="{{CONVENTIONS}}"))
        self.assertError("unfilled placeholders")

    def test_bad_autonomy_level(self):
        self.org["autonomy_level"] = "L9"
        self.save()
        self.assertError("autonomy_level")

    def test_active_learnings_over_budget(self):
        write(self.root, ".claude/ceo/learnings/_shared.md", "## Active\n" + "- x\n" * 61 + "## Archive\n")
        self.assertError("demote")

    def test_guard_not_wired(self):
        write(self.root, ".claude/settings.json", "{}")
        self.assertError("not registered")

    def test_perimeter_covering_org_files(self):
        self.org["agents"][0]["perimeter"] = [".claude/**"]
        self.save()
        self.assertError("covers org files")

    def test_perimeter_except_excludes_org_files(self):
        self.org["agents"][0]["perimeter"] = [".claude/**"]
        self.org["agents"][0]["except"] = [".claude/agents/**", ".claude/ceo/**", ".claude/skills/demo-ceo/**",
                                           ".claude/hooks/**"]
        self.save()
        code, out = self.doctor()
        self.assertFalse(any("covers org files" in e for e in out["errors"]), out)

    def test_user_data_and_ignored_refs_do_not_warn(self):
        write(self.root, ".gitignore", "output/\n")
        self.org["user_data_paths"] = ["config/profile.yml", "data/*"]
        self.save()
        write(self.root, ".claude/agents/demo-frontend-engineer.md", agent(
            "demo-frontend-engineer", body="Never touch `config/profile.yml`, `data/apps.md` or `output/cv.pdf`; see `src/gone.ts`."))
        code, out = self.doctor()
        refs = [w for w in out["warnings"] if "does not exist" in w]
        self.assertEqual(len(refs), 1, refs)
        self.assertIn("src/gone.ts", refs[0])

    def test_fill_comment_left_in(self):
        write(self.root, ".claude/agents/demo-frontend-engineer.md", agent("demo-frontend-engineer", body="<!-- FILL: conventions -->"))
        self.assertError("FILL")

    def test_editor_without_eval_warns(self):
        os.remove(os.path.join(self.root, ".claude", "ceo", "evals", "cases", "c1.md"))
        code, out = self.doctor()
        self.assertEqual(code, 0)
        self.assertTrue(any("no eval case" in w for w in out["warnings"]))


if __name__ == "__main__":
    unittest.main()
