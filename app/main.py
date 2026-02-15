import argparse
import logging

from kernel.kernel import Kernel
from orchestrator.default_orchestrator import DefaultOrchestrator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default = "WARNING", help = "Logging level (DEBUG, INFO, WARNING, ERROR)")
    args = parser.parse_args()
    logging.basicConfig(level = getattr(logging, args.log.upper(), logging.WARNING))

    kernel = Kernel()
    orchestrator = DefaultOrchestrator()

    kernel.run(orchestrator)

if __name__ == "__main__":
    main()
