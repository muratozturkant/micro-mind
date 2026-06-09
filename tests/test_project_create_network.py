import json
import tempfile
import unittest
from pathlib import Path

from micro_mind.core.root_planner import RootPlanner
from micro_mind.nodes.base_node import BaseNode
from micro_mind.nodes.memory_node import MemoryNode


class ProjectCreateNetworkTest(unittest.TestCase):
    def test_root_planner_creates_verifies_remembers_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target_directory = Path(temp_dir) / "projects"

            planner = RootPlanner()
            first_result = planner.execute(
                task="create_project_structure",
                project_name="Block Heaven",
                project_type="flutter",
                target_directory=target_directory,
            )

            project_root = target_directory / "block_heaven"
            required_directories = [
                "frontend",
                "backend",
                "database",
                "docs",
                ".micro_mind",
                ".micro_mind/executions",
                ".micro_mind/nodes",
            ]
            required_files = ["PROJECT_STATE.md", "DEVELOPMENT_RULES.md"]

            self.assertEqual(first_result["result"], "success")
            self.assertEqual(first_result["project_name"], "block_heaven")
            self.assertEqual(first_result["project_type"], "flutter")
            self.assertTrue(first_result["verification_result"]["success"])
            self.assertEqual(first_result["verification_result"]["missing_directories"], [])
            self.assertEqual(first_result["verification_result"]["missing_files"], [])

            for relative_path in required_directories:
                self.assertTrue((project_root / relative_path).is_dir())

            for relative_path in required_files:
                self.assertTrue((project_root / relative_path).is_file())

            self.assertEqual(
                first_result["nodes_used"],
                [
                    "QuestionNode",
                    "DirectoryCreateNode",
                    "StructureVerifyNode",
                    "MemoryNode",
                ],
            )
            self.assertEqual(len(first_result["created_directories"]), len(required_directories))
            self.assertEqual(len(first_result["created_files"]), len(required_files))

            memory_path = Path(first_result["memory_file"])
            self.assertTrue(memory_path.is_file())
            memory = json.loads(memory_path.read_text(encoding="utf-8"))
            self.assertEqual(memory["task"], "create_project_structure")
            self.assertEqual(memory["project_name"], "block_heaven")
            self.assertEqual(memory["project_type"], "flutter")
            self.assertEqual(memory["target_directory"], str(target_directory))
            self.assertEqual(memory["result"], "success")
            self.assertTrue(memory["verification_result"]["success"])
            self.assertEqual(memory["nodes_used"], first_result["nodes_used"])
            self.assertIsInstance(memory["duration_seconds"], float)
            self.assertIsInstance(memory["timestamp"], str)

            question_stats_path = project_root / ".micro_mind" / "nodes" / "QuestionNode.json"
            question_stats = json.loads(question_stats_path.read_text(encoding="utf-8"))
            self.assertEqual(question_stats["node_name"], "QuestionNode")
            self.assertEqual(question_stats["activation_count"], 1)
            self.assertEqual(question_stats["success_count"], 1)
            self.assertEqual(question_stats["failure_count"], 0)
            self.assertEqual(question_stats["state"], "SLEEPING")
            self.assertIsInstance(question_stats["sleep_score"], float)
            self.assertIsInstance(question_stats["fitness_score"], float)

            second_result = planner.execute(
                task="create_project_structure",
                project_name="Block Heaven",
                project_type="flutter",
                target_directory=target_directory,
            )

            self.assertEqual(second_result["result"], "success")
            self.assertEqual(second_result["created_directories"], [])
            self.assertEqual(second_result["created_files"], [])
            self.assertTrue(second_result["verification_result"]["success"])

            updated_question_stats = json.loads(question_stats_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_question_stats["activation_count"], 2)
            self.assertEqual(updated_question_stats["success_count"], 2)
            self.assertEqual(updated_question_stats["failure_count"], 0)

    def test_memory_node_uses_base_lifecycle_and_persists_success_stats(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target_directory = Path(temp_dir) / "projects"

            self.assertIs(MemoryNode.run, BaseNode.run)

            result = RootPlanner().execute(
                task="create_project_structure",
                project_name="Memory Stats",
                project_type="flutter",
                target_directory=target_directory,
            )

            memory_stats_path = (
                Path(result["project_root"])
                / ".micro_mind"
                / "nodes"
                / "MemoryNode.json"
            )
            memory_stats = json.loads(memory_stats_path.read_text(encoding="utf-8"))

            self.assertEqual(memory_stats["activation_count"], 1)
            self.assertEqual(memory_stats["success_count"], 1)
            self.assertEqual(memory_stats["failure_count"], 0)
            self.assertEqual(memory_stats["fitness_score"], 1.0)
            self.assertEqual(memory_stats["state"], "SLEEPING")


if __name__ == "__main__":
    unittest.main()
