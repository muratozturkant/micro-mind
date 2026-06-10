import json
import tempfile
import unittest
from pathlib import Path

from micro_mind.core.context.execution_context import ExecutionContext
from micro_mind.core.root_planner import RootPlanner


class ExecutionContextTest(unittest.TestCase):
    def test_execution_context_defaults_are_safe_mutable_values(self):
        first = ExecutionContext(task_type="create_project_structure")
        second = ExecutionContext(task_type="create_project_structure")

        first.created_directories.append(Path("frontend"))
        first.verification_result["success"] = True
        first.execution_memory["task_id"] = first.task_id
        first.metadata["nodes_used"] = ["QuestionNode"]

        self.assertNotEqual(first.task_id, second.task_id)
        self.assertEqual(second.created_directories, [])
        self.assertEqual(second.verification_result, {})
        self.assertEqual(second.execution_memory, {})
        self.assertEqual(second.metadata, {})

    def test_project_create_network_uses_context_without_changing_result_shape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = RootPlanner().execute(
                task="create_project_structure",
                project_name="Context Project",
                project_type="flutter",
                target_directory=Path(temp_dir) / "projects",
            )

            expected_keys = {
                "task",
                "project_name",
                "project_type",
                "target_directory",
                "project_root",
                "result",
                "nodes_used",
                "duration_seconds",
                "created_directories",
                "created_files",
                "verification_result",
                "memory_file",
            }
            self.assertEqual(set(result.keys()), expected_keys)

            memory = json.loads(Path(result["memory_file"]).read_text(encoding="utf-8"))
            self.assertEqual(memory["task"], "create_project_structure")
            self.assertNotIn("task_id", result)
            self.assertIsInstance(memory["task_id"], str)
            self.assertEqual(memory["project_name"], "context_project")
            self.assertEqual(memory["project_type"], "flutter")
            self.assertTrue(memory["verification_result"]["success"])


if __name__ == "__main__":
    unittest.main()
