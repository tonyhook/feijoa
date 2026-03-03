import argparse
import logging

from agents.executor_agent import ExecutorAgent
from agents.judge_agent import JudgeAgent
from agents.planner.llm_fallback import LLMFallbackPlanner
from agents.planner.planner_movie_releasedate import MovieReleaseDatePlanner
from kernel.kernel import Kernel
from memory.local_file_memory import LocalFileMemory
from orchestrator.default_orchestrator import DefaultOrchestrator
from tools.llm import LLMTool
from tools.movie_releasedate import MovieReleaseDateTool
from tracing.local_file_trace import LocalFileTrace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default = "WARNING", help = "Logging level (DEBUG, INFO, WARNING, ERROR)")
    args = parser.parse_args()
    logging.basicConfig(level = getattr(logging, args.log.upper(), logging.WARNING))

    memory = LocalFileMemory("session.json")
    trace = LocalFileTrace("trace.json")
    kernel = Kernel(memory = memory, trace = trace)
    orchestrator = DefaultOrchestrator()

    kernel.register_agent(MovieReleaseDatePlanner("movie_releasedate"))
    kernel.register_agent(LLMFallbackPlanner("llm_fallback"))

    kernel.register_agent(JudgeAgent("judge"))
    kernel.register_agent(ExecutorAgent("executor"))

    kernel.register_tool(LLMTool("llm"))
    kernel.register_tool(MovieReleaseDateTool("movie_releasedate"))

    try:
        while True:
            kernel.run(orchestrator)
            kernel._reset_round()
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
