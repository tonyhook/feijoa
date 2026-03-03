from agents.planner_agent import PlannerAgent
from kernel.kernel import Kernel
from kernel.plan import NotApplicable, Plan, Step
from tools.extract_movie_title import extract_movie_title


class MovieReleaseDatePlanner(PlannerAgent):

    def plan(self, kernel: Kernel) -> Plan | NotApplicable:
        # If the user resolved a clarification, use the pre-resolved movie directly
        resolved = kernel.clarification_resolved
        if resolved:
            return Plan(
                planner = self.name,
                priority = 10,
                steps = [
                    Step(
                        tool = "movie_releasedate",
                        input = {
                            "title": resolved.data["title"],
                            "imdb_id": resolved.data["id"],
                            "year": resolved.data["year"],
                        }
                    )
                ]
            )

        title = extract_movie_title(kernel.input)
        if not title:
            return NotApplicable(
                planner = self.name,
                reason = "not a movie release date question"
            )

        return Plan(
            planner = self.name,
            priority = 10,
            steps =[
                Step(
                    tool = "movie_releasedate",
                    input = {"title": title}
                )
            ]
        )
