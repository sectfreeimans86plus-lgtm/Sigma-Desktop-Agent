from src.core.banner import show_banner
from src.core.logger import logger


def startup():

    logger.info("Starting Sigma AI Desktop Agent...")

    show_banner()

    logger.success("Startup Completed Successfully")