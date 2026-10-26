"""Tests for templates/hooks/org_guard.py. Run: python3 -m unittest discover tests"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

GUARD = os.path.join(os.path.dirname(__file__), "..", "skills", "org-init", "templates", "hooks", "org_guard.py")


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, ".claude", "ceo"))
        self.set_org({"base_branch": "main", "autonomy_level": "L1",
                      "gate_files": ["tsconfig.json"], "guard": {"block_stash": True}})

    def set_org(self, org):
        with open(os.path.join(self.root, ".claude", "ceo", "org.json"), "w") as f:
            json.dump(org, f)

    def run_guard(self, mode, tool_input):
        res = subprocess.run([sys.executable, GUARD, mode], input=json.dumps({"tool_input": tool_input}),
                             capture_output=True, text=True, env={**os.environ, "CLAUDE_PROJECT_DIR": self.root})
        return res.returncode

    def bash(self, cmd):
        return self.run_guard("bash", {"command": cmd})

    def test_blocks_admin_merge(self):
        self.set_org({"autonomy_level": "L4"})
        self.assertEqual(self.bash("gh pr merge 12 --squash --admin"), 2)

    def test_merge_blocked_below_l3_allowed_at_l3(self):
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 2)
        self.set_org({"autonomy_level": "L3"})
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 0)

    def test_missing_org_defaults_to_no_merge(self):
        os.remove(os.path.join(self.root, ".claude", "ceo", "org.json"))
        self.assertEqual(self.bash("gh pr merge 12"), 2)

    def test_force_push(self):
        self.assertEqual(self.bash("git push --force origin org/x"), 2)
        self.assertEqual(self.bash("git push -f origin org/x"), 2)
        self.assertEqual(self.bash("git push --force-with-lease origin org/x"), 0)
        self.assertEqual(self.bash("git push --force-with-lease origin main"), 2)

    def test_push_to_base(self):
        self.assertEqual(self.bash("git push origin main"), 2)
        self.assertEqual(self.bash("git push origin HEAD:main"), 2)
        self.assertEqual(self.bash("git push -u origin org/main-fix"), 0)
        self.assertEqual(self.bash("git push origin maintenance"), 0)

    def test_no_verify(self):
        self.assertEqual(self.bash("git commit -m x --no-verify"), 2)

    def test_stash(self):
        self.assertEqual(self.bash("git stash"), 2)
        self.assertEqual(self.bash("git stash push -u -m wip"), 2)
        self.assertEqual(self.bash("cd x && git stash pop"), 2)
        self.assertEqual(self.bash("git stash list"), 0)
        self.set_org({"guard": {"block_stash": False}})
        self.assertEqual(self.bash("git stash"), 0)

    def test_quoted_text_does_not_trigger(self):
        # The pattern quoted inside a commit message or PR body is not a command.
        self.assertEqual(self.bash('git commit -m "guard blocks git stash and gh pr merge --admin"'), 0)
        self.assertEqual(self.bash("git status"), 0)

    def test_edit_gate_file(self):
        path = os.path.join(self.root, "tsconfig.json")
        open(path, "w").close()
        self.assertEqual(self.run_guard("edit", {"file_path": path}), 2)
        self.assertEqual(self.run_guard("edit", {"file_path": os.path.join(self.root, "new", "tsconfig.json")}), 0)
        other = os.path.join(self.root, "a.ts")
        open(other, "w").close()
        self.assertEqual(self.run_guard("edit", {"file_path": other}), 0)

    def test_human_escape_hatch_for_gate_edits(self):
        path = os.path.join(self.root, "tsconfig.json")
        open(path, "w").close()
        open(os.path.join(self.root, ".claude", "ceo", "ALLOW_GATE_EDITS"), "w").close()
        self.assertEqual(self.run_guard("edit", {"file_path": path}), 0)

    def test_stop_check_runs_once_per_batch(self):
        os.makedirs(os.path.join(self.root, "src"))
        open(os.path.join(self.root, "src", "a.ts"), "w").close()
        self.set_org({"guard": {"stop_check": {"cmd": "echo 'error TS1' && exit 1", "watch": ["src"], "extensions": [".ts"]}}})
        self.assertEqual(self.run_guard("stop", {}), 2)
        self.assertEqual(self.run_guard("stop", {}), 0)  # stamped: never loops

    def test_stop_check_disabled(self):
        self.set_org({"guard": {"stop_check": {"cmd": ""}}})
        self.assertEqual(self.run_guard("stop", {}), 0)

    def test_garbage_input_never_blocks(self):
        res = subprocess.run([sys.executable, GUARD, "bash"], input="not json", capture_output=True, text=True,
                             env={**os.environ, "CLAUDE_PROJECT_DIR": self.root})
        self.assertEqual(res.returncode, 0)


if __name__ == "__main__":
    unittest.main()
