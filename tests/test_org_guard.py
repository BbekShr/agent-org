"""Tests for templates/hooks/org_guard.py. Run: python3 -m unittest discover tests"""
import json
import os
import subprocess
import sys
import tempfile
import time
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

    def run_guard(self, mode, tool_input, org_run=True):
        env = {**os.environ, "CLAUDE_PROJECT_DIR": self.root}
        env.pop("AGENT_ORG_RUN", None)
        if org_run:
            env["AGENT_ORG_RUN"] = "1"
        res = subprocess.run([sys.executable, GUARD, mode], input=json.dumps({"tool_input": tool_input}),
                             capture_output=True, text=True, env=env)
        return res.returncode

    def bash(self, cmd, org_run=True):
        return self.run_guard("bash", {"command": cmd}, org_run)

    def test_blocks_admin_merge(self):
        self.set_org({"autonomy_level": "L4"})
        self.assertEqual(self.bash("gh pr merge 12 --squash --admin"), 2)

    def test_merge_blocked_below_l3_allowed_at_l3(self):
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 2)
        self.set_org({"autonomy_level": "L3"})
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 0)

    def test_missing_org_defaults_to_no_merge_during_a_run(self):
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

    def test_human_session_is_not_bound_by_org_rules(self):
        # Outside an org run, the human's own sessions may merge, push to main and stash.
        self.assertEqual(self.bash("gh pr merge 12 --squash", org_run=False), 0)
        self.assertEqual(self.bash("git push origin main", org_run=False), 0)
        self.assertEqual(self.bash("git stash push -u -m wip", org_run=False), 0)
        # ...but the always-wrong commands stay blocked for everyone.
        self.assertEqual(self.bash("gh pr merge 12 --admin", org_run=False), 2)
        self.assertEqual(self.bash("git push --force origin x", org_run=False), 2)
        self.assertEqual(self.bash("git commit -m x --no-verify", org_run=False), 2)

    def test_run_marker_activates_and_expires(self):
        cache = os.path.join(self.root, ".claude", "ceo", ".cache")
        os.makedirs(cache)
        marker = os.path.join(cache, "run-active")
        open(marker, "w").close()
        self.assertEqual(self.bash("git stash", org_run=False), 2)
        old = time.time() - 13 * 3600
        os.utime(marker, (old, old))
        self.assertEqual(self.bash("git stash", org_run=False), 0)

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

    def touch(self, rel):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").close()
        return path

    def test_control_files_blocked_even_when_not_in_gate_files(self):
        self.set_org({"gate_files": []})
        for rel in (".claude/ceo/org.json", ".claude/ceo/AUTONOMY.md", ".claude/settings.json",
                    ".claude/hooks/org_guard.py"):
            path = self.touch(rel) if rel != ".claude/ceo/org.json" else os.path.join(self.root, rel)
            self.assertEqual(self.run_guard("edit", {"file_path": path}), 2, rel)
            self.assertEqual(self.run_guard("edit", {"file_path": path}, org_run=False), 2, rel)
        # Matched on the repo-relative path: an unrelated org.json elsewhere is fine.
        self.assertEqual(self.run_guard("edit", {"file_path": self.touch("packages/x/org.json")}), 0)

    def test_control_file_escape_hatch(self):
        self.touch(".claude/ceo/ALLOW_GATE_EDITS")
        path = os.path.join(self.root, ".claude", "ceo", "org.json")
        self.assertEqual(self.run_guard("edit", {"file_path": path}), 0)

    def test_shell_writes_to_control_files_blocked_during_a_run(self):
        for cmd in ("echo '{}' > .claude/ceo/org.json", "sed -i '' 's/L1/L3/' .claude/ceo/org.json",
                    "cat x | tee .claude/settings.json", "cp evil.py .claude/hooks/org_guard.py",
                    "rm .claude/ceo/DEMOTED"):
            self.assertEqual(self.bash(cmd), 2, cmd)
            self.assertEqual(self.bash(cmd, org_run=False), 0, cmd)
        self.assertEqual(self.bash("cat .claude/ceo/org.json"), 0)
        self.assertEqual(self.bash("git diff .claude/settings.json > /tmp/d"), 0)

    def test_demoted_file_lowers_the_level(self):
        self.set_org({"autonomy_level": "L3"})
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 0)
        with open(self.touch(".claude/ceo/DEMOTED"), "w") as f:
            f.write("L1\n")
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 2)
        with open(os.path.join(self.root, ".claude", "ceo", "DEMOTED"), "w") as f:
            f.write("L4")  # can't raise above org.json
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 0)
        self.set_org({"autonomy_level": "L1"})
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 2)
        with open(os.path.join(self.root, ".claude", "ceo", "DEMOTED"), "w") as f:
            f.write("garbage")  # unreadable level fails safe
        self.set_org({"autonomy_level": "L3"})
        self.assertEqual(self.bash("gh pr merge 12 --squash"), 2)

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
