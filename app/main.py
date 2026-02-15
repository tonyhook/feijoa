
from kernel.kernel import Kernel
from orchestrator.default_orchestrator import DefaultOrchestrator


def main():
    kernel = Kernel()
    orchestrator = DefaultOrchestrator()

    kernel.run(orchestrator)

if __name__ == "__main__":
    main()
