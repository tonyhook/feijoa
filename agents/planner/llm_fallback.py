from agents.planner_agent import PlannerAgent
from kernel.kernel import Kernel
from kernel.plan import Plan, Step


class LLMFallbackPlanner(PlannerAgent):

    def plan(self, kernel: Kernel):
        return Plan(
            planner = self.name,
            steps = [
                Step(
                    tool = "llm",
                    input = {"text": kernel.input}
                )
            ]
        )
