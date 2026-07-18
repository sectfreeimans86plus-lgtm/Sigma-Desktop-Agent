from pathlib import Path
from loguru import logger
import sys

# Project Root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Logs Folder
LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log File
LOG_FILE = LOG_DIR / "sigma.log"

# Remove Default Logger
logger.remove()

# Console Output
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
)

# File Output
logger.add(
    LOG_FILE,
    rotation="5 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG",
)

logger.info("Logger Initialized Successfully")