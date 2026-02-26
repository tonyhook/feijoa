
from agents.executor_agent import ExecutorAgent
from agents.judge_agent import JudgeAgent
from agents.planner.llm_fallback import LLMFallbackPlanner
from kernel.kernel import Kernel
from memory.local_file_memory import LocalFileMemory
from orchestrator.default_orchestrator import DefaultOrchestrator
from tools.llm import LLMTool
from tracing.local_file_trace import LocalFileTrace


def main():
    memory = LocalFileMemory("session.json")
    trace = LocalFileTrace("trace.json")
    kernel = Kernel(memory = memory, trace = trace)
    orchestrator = DefaultOrchestrator()

    kernel.register_agent(LLMFallbackPlanner("llm_fallback"))

    kernel.register_agent(JudgeAgent("judge"))
    kernel.register_agent(ExecutorAgent("executor"))

    kernel.register_tool(LLMTool("llm"))

    kernel.run(orchestrator)

if __name__ == "__main__":
    main()
