import argparse
import logging

from agents.executor_agent import ExecutorAgent
from agents.judge_agent import JudgeAgent
from agents.planner.llm_fallback import LLMFallbackPlanner
from kernel.kernel import Kernel
from orchestrator.default_orchestrator import DefaultOrchestrator
from tools.llm import LLMTool


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default = "WARNING", help = "Logging level (DEBUG, INFO, WARNING, ERROR)")
    args = parser.parse_args()
    logging.basicConfig(level = getattr(logging, args.log.upper(), logging.WARNING))

    kernel = Kernel()
    orchestrator = DefaultOrchestrator()

    kernel.register_agent(LLMFallbackPlanner("llm_fallback"))

    kernel.register_agent(JudgeAgent("judge"))
    kernel.register_agent(ExecutorAgent("executor"))

    kernel.register_tool(LLMTool("llm"))

    kernel.run(orchestrator)

if __name__ == "__main__":
    main()
