from agents.planner_agent import PlannerAgent
from kernel.kernel import Kernel
from kernel.plan import Plan, Step


class LLMFallbackPlanner(PlannerAgent):

    def plan(self, kernel: Kernel):
        if kernel.memory:
            context = str(kernel.memory.get_context())
        else:
            context = kernel.input

        return Plan(
            planner = self.name,
            steps = [
                Step(
                    tool = "llm",
                    input = {"text": context}
                )
            ]
        )
