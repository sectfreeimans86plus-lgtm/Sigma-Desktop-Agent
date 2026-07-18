"""
=========================================
 Sigma AI Desktop Agent
 Main Entry Point
=========================================
"""

import sys
import time

from src.core.startup import startup
from src.core.agent import SigmaAgent
from src.core.logger import logger


def initialize():
    """
    Initialize all startup services.
    """

    logger.info("Initializing Application...")

    startup()


def run_agent():
    
    """
    Create and start Sigma AI Agent.
    """

    agent = SigmaAgent()
    agent.start()
    agent.recall_latest_memory()
    return agent


def shutdown():
    """
    Clean shutdown.
    """

    logger.warning("Application Shutdown Requested.")

    logger.success("Sigma AI Desktop Agent Closed Successfully.")


def main():

    start_time = time.time()

    try:

        initialize()

        agent = run_agent()

        logger.info(
            f"Current Agent Status : {agent.get_status()}"
        )

        latest_memory = agent.recall_latest_memory()

        if latest_memory:

            print("\n========== LAST MEMORY ==========")
            print(f"Category : {latest_memory[0]}")
            print(f"Content  : {latest_memory[1]}")
            print(f"Created  : {latest_memory[2]}")
            print("=================================\n")
        response = agent.ask("Hello Sigma")

        print("\n========== AI RESPONSE ==========")
        print(response)
        print("=================================\n")
    except KeyboardInterrupt:

        logger.warning("Keyboard Interrupt Received.")

    except Exception as error:

        logger.exception(error)

    finally:

        shutdown()

        execution_time = round(time.time() - start_time, 2)

        logger.info(
            f"Execution Time : {execution_time} seconds"
        )

        sys.exit(0)


if __name__ == "__main__":
    main()