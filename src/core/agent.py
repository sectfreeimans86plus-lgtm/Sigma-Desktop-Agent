from src.core.logger import logger
from src.database.memory import MemoryManager
from src.ai.brain import Brain
from src.tools.desktop import DesktopController
from src.ai.intent import IntentEngine

class SigmaAgent:

    def __init__(self):

        self.memory = MemoryManager()
        self.brain = Brain()
        self.intent = IntentEngine()
        self.desktop = DesktopController()
        self.name = "Sigma AI Desktop Agent"
        self.version = "1.1.0"
        self.status = "Initializing"

        logger.info("=" * 60)
        logger.info(f"{self.name} Initializing...")
        logger.info("=" * 60)

    # ---------------------------------------------------------

    def start(self):

        self.status = "Running"

        self.brain.set_provider("Local")

        self.memory.save_memory(
            "system",
            f"{self.name} Started Successfully"
        )

        logger.success(f"{self.name} Started Successfully")

    # ---------------------------------------------------------

    def stop(self):

        self.status = "Stopped"

        self.memory.save_memory(
            "system",
            f"{self.name} Stopped Successfully"
        )

        logger.warning(f"{self.name} Stopped")

    # ---------------------------------------------------------

    def get_status(self):

        return self.status

    # ---------------------------------------------------------

    def recall_latest_memory(self):

        memory = self.memory.latest_memory()

        if memory:
            logger.info(f"Latest Memory : {memory}")

        return memory

    # ---------------------------------------------------------

    def execute_desktop_command(self, message):

        text = message.lower().strip()

        apps = self.desktop.list_supported_apps()

        for app in apps:

            if app in text:

                logger.info(f"Desktop Command Detected : {app}")

                success = self.desktop.open_application(app)

                if success:
                    return f"{app.title()} opened successfully."

                return f"Unable to open {app}."

        return None

    # ---------------------------------------------------------

    def ask(self, message):

        logger.info("=" * 60)
        logger.info(f"User : {message}")

        desktop_response = self.execute_desktop_command(message)

        if desktop_response:

            self.memory.save_memory("user", message)
            self.memory.save_memory("assistant", desktop_response)

            logger.success(desktop_response)

            return desktop_response

        memory = self.memory.latest_memory()

        response = self.brain.chat(
            message=message,
            memory=memory
        )

        self.memory.save_memory("user", message)
        self.memory.save_memory("assistant", response)

        logger.info(f"Assistant : {response}")

        return response

    # ---------------------------------------------------------

    def memory_count(self):

        return self.memory.memory_count()

    # ---------------------------------------------------------

    def save_note(self, category, content):

        self.memory.save_memory(category, content)

        logger.info(f"Memory Saved : {category}")

    # ---------------------------------------------------------

    def info(self):

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "provider": self.brain.get_provider(),
            "memory_count": self.memory.memory_count(),
            "supported_apps": self.desktop.list_supported_apps()
        }