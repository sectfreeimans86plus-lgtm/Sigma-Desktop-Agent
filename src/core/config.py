from pathlib import Path

# ==========================
# Project Paths
# ==========================

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "memory.db"
import platform

# ===============================
# Project Information
# ===============================

PROJECT_NAME = "Sigma AI Desktop Agent"

VERSION = "1.0.0"

AUTHOR = "Sigma"

COMPANY = "Sigma Development"

DESCRIPTION = "Personal AI Desktop Assistant"


# ===============================
# Environment
# ===============================

ENVIRONMENT = "Development"

DEBUG = True


# ===============================
# Project Paths
# ===============================

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

SRC_DIR = ROOT_DIR / "src"

DATA_DIR = ROOT_DIR / "data"

LOG_DIR = ROOT_DIR / "logs"

CONFIG_DIR = ROOT_DIR / "config"

ASSETS_DIR = ROOT_DIR / "assets"

DOCS_DIR = ROOT_DIR / "docs"

TESTS_DIR = ROOT_DIR / "tests"

SCRIPTS_DIR = ROOT_DIR / "scripts"


# ===============================
# AI Settings
# ===============================

DEFAULT_AI_PROVIDER = "OpenAI"

DEFAULT_MODEL = "gpt-5"

TEMPERATURE = 0.7

MAX_TOKENS = 4096


# ===============================
# Browser
# ===============================

DEFAULT_BROWSER = "Chrome"

HEADLESS = False


# ===============================
# Voice
# ===============================

VOICE_ENABLED = False


# ===============================
# Vision
# ===============================

VISION_ENABLED = False


# ===============================
# Database
# ===============================

DATABASE_NAME = "sigma.db"


# ===============================
# System Information
# ===============================

OPERATING_SYSTEM = platform.system()

PYTHON_VERSION = platform.python_version()