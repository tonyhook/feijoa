from kernel.event import Event, EventType
from kernel.kernel import Kernel
from kernel.phase import Phase
from orchestrator.orchestrator import Orchestrator


class DefaultOrchestrator(Orchestrator):

    def _all_planner_responsed(self) -> bool:
        return True

    def handle(self, kernel: Kernel):
        # event from judge / simulator / executor, transition phase accordingly
        while kernel.events:
            event: Event = kernel.events.pop(0)

            # plan selected, transition to simulationß
            if kernel.phase == Phase.DECISION and event.type == EventType.PLAN_SELECTED:
                kernel.set_phase(Phase.SIMULATION)

            # simulation finished, transition to execution
            elif kernel.phase == Phase.SIMULATION and event.type == EventType.SIMULATION_RESULT:
                # TODO: we can have more complex logic here, e.g. if the simulation result is bad, we can go back to decision phase
               kernel.set_phase(Phase.EXECUTION)

            # execution finished, transition to finished
            elif kernel.phase == Phase.EXECUTION and event.type == EventType.EXECUTION_RESULT:
                # TODO: we can have more complex logic here, e.g. if the execution result is bad, we can go back to decision phase
                kernel.set_phase(Phase.FINISHED)

        # event from planners, transition phase accordingly
        if kernel.phase == Phase.PLANNING:
            if self._all_planner_responsed():
                kernel.set_phase(Phase.DECISION)
