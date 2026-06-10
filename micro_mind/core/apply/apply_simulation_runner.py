

from micro_mind.core.apply.apply_plan_builder import ApplyPlanBuilder
from micro_mind.core.apply.apply_simulator import ApplySimulator


class ApplySimulationRunner:
    def __init__(
        self,
        apply_plan_builder: ApplyPlanBuilder | None = None,
        apply_simulator: ApplySimulator | None = None,
    ):
        self.apply_plan_builder = apply_plan_builder or ApplyPlanBuilder()
        self.apply_simulator = apply_simulator or ApplySimulator()

    def run(self, simulation_report: dict | None) -> dict:
        apply_plan = self.apply_plan_builder.build(simulation_report)

        if apply_plan.get("status") != "apply_plan_created":
            return {
                "status": "waiting_for_human_guidance",
                "reason": "apply_plan_failed",
                "apply_plan": apply_plan,
                "apply_simulation": None,
            }

        apply_simulation = self.apply_simulator.simulate(apply_plan)

        if apply_simulation.get("status") != "apply_simulated":
            return {
                "status": "waiting_for_human_guidance",
                "reason": "apply_simulation_failed",
                "apply_plan": apply_plan,
                "apply_simulation": apply_simulation,
            }

        return {
            "status": "apply_ready_for_human_approval",
            "requires_human_approval": True,
            "will_write_real_files": False,
            "will_run_commands": False,
            "would_write_real_files_after_approval": apply_simulation.get(
                "would_write_real_files_after_approval", False
            ),
            "would_run_commands_after_approval": apply_simulation.get(
                "would_run_commands_after_approval", False
            ),
            "apply_plan": apply_plan,
            "apply_simulation": apply_simulation,
        }