import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SDDScaffoldTests(unittest.TestCase):
    def test_agent_topology(self):
        data = json.loads((ROOT / "config/agents.json").read_text(encoding="utf-8"))
        agents = data["agents"]
        self.assertEqual(len(agents), 100)
        self.assertEqual(sum(a["role"] == "director" for a in agents), 1)
        self.assertEqual(sum(a["role"] == "coordinator" for a in agents), 9)
        self.assertEqual(sum(a["role"] == "specialist" for a in agents), 90)

    def test_policy_blocks_production_and_cost(self):
        p = json.loads((ROOT / "config/policy.json").read_text(encoding="utf-8"))
        self.assertEqual(p["default_budget_eur"], 0)
        self.assertFalse(p["production_deploy_allowed"])
        self.assertTrue(p["human_approval_required"])

    def test_required_docs(self):
        for f in ["docs/SPEC.md", "docs/PLAN.md", "docs/TASKS.md", "docs/QUALITY_GATES.md"]:
            self.assertTrue((ROOT / f).is_file(), f)

if __name__ == "__main__":
    unittest.main()
