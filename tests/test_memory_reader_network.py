import json
import tempfile
import unittest
from pathlib import Path

from micro_mind.core.root_planner import RootPlanner


class MemoryReaderNetworkTest(unittest.TestCase):
    def test_summarizes_existing_project_memory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target_directory = Path(temp_dir) / "projects"
            planner = RootPlanner()
            project_result = planner.execute(
                task="create_project_structure",
                project_name="Block Heaven",
                project_type="flutter",
                target_directory=target_directory,
            )

            summary = planner.execute(
                task="memory_summary",
                project_root=Path(project_result["project_root"]),
            )

            self.assertEqual(summary["project_root"], project_result["project_root"])
            self.assertEqual(summary["total_executions"], 1)
            self.assertEqual(summary["successful_executions"], 1)
            self.assertEqual(summary["failed_executions"], 0)
            self.assertIsInstance(summary["last_execution"], str)
            self.assertEqual(summary["tasks_seen"], ["create_project_structure"])
            self.assertGreater(summary["average_duration_seconds"], 0)
            self.assertIn("QuestionNode", summary["node_stats"])
            self.assertIn("MemoryNode", summary["node_stats"])
            most_used = {
                node["node_name"]: node["activation_count"]
                for node in summary["most_used_nodes"]
            }
            self.assertEqual(most_used["QuestionNode"], 1)
            self.assertEqual(most_used["MemoryNode"], 1)

    def test_handles_missing_micro_mind_folder_gracefully(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "missing_memory_project"
            project_root.mkdir()

            summary = RootPlanner().execute(
                task="memory_summary",
                project_root=project_root,
            )

            self.assertEqual(summary["project_root"], str(project_root))
            self.assertEqual(summary["total_executions"], 0)
            self.assertEqual(summary["successful_executions"], 0)
            self.assertEqual(summary["failed_executions"], 0)
            self.assertIsNone(summary["last_execution"])
            self.assertEqual(summary["tasks_seen"], [])
            self.assertEqual(summary["node_stats"], {})
            self.assertEqual(summary["most_used_nodes"], [])
            self.assertEqual(summary["average_duration_seconds"], 0.0)

    def test_handles_empty_memory_folders_gracefully(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "empty_memory_project"
            (project_root / ".micro_mind" / "executions").mkdir(parents=True)
            (project_root / ".micro_mind" / "nodes").mkdir(parents=True)

            summary = RootPlanner().execute(
                task="memory_summary",
                project_root=project_root,
            )

            self.assertEqual(summary["total_executions"], 0)
            self.assertEqual(summary["node_stats"], {})
            self.assertEqual(summary["most_used_nodes"], [])

    def test_cli_prints_memory_summary_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target_directory = Path(temp_dir) / "projects"
            project_result = RootPlanner().execute(
                task="create_project_structure",
                project_name="Cli Summary",
                project_type="flutter",
                target_directory=target_directory,
            )

            from micro_mind.cli.create_project import build_parser

            parser = build_parser()
            args = parser.parse_args(
                ["memory-summary", "--project", project_result["project_root"]]
            )

            self.assertEqual(args.command, "memory-summary")
            self.assertEqual(args.project, Path(project_result["project_root"]))


if __name__ == "__main__":
    unittest.main()
