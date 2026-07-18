"""
=========================================
Sigma AI - Intent Engine
Version : 3.0 (Part 1A)
=========================================
"""

from typing import Dict, Optional
from src.core.logger import logger


class IntentEngine:
    """
    Sigma Intent Detection Engine
    """

    def __init__(self):

        self.name = "Sigma Intent Engine"

        logger.info(f"{self.name} initialized successfully.")

        # -----------------------------
        # Open Keywords
        # -----------------------------

        self.open_keywords = [
            "open",
            "launch",
            "start",
            "run",
            "execute",
            "open up",

            # Roman Urdu
            "khol",
            "kholo",
            "khol do",
            "kholo",
            "chalao",
            "chala do",
            "start karo",
            "run karo",
        ]

        # -----------------------------
        # Application Aliases
        # -----------------------------

        self.application_map = {

            # Browsers
            "chrome": "chrome",
            "google chrome": "chrome",
            "browser": "chrome",

            "edge": "edge",
            "microsoft edge": "edge",

            "firefox": "firefox",

            # Editors
            "notepad": "notepad",
            "notepad++": "notepad",

            "vscode": "vscode",
            "vs code": "vscode",
            "visual studio code": "vscode",

            # Windows Apps
            "calculator": "calculator",
            "calc": "calculator",

            "paint": "paint",
            "mspaint": "paint",

            "cmd": "cmd",
            "command prompt": "cmd",

            "powershell": "powershell",

            "explorer": "explorer",
            "file explorer": "explorer",
        }

    # =====================================
    # Normalize Text
    # =====================================

    def normalize_text(self, text: str) -> str:
        return text.lower().strip()

    # =====================================
    # Normalize Application Name
    # =====================================

    def normalize_application(self, app: str) -> Optional[str]:

        app = self.normalize_text(app)

        for alias, original in self.application_map.items():

            if alias == app:
                return original

        return None
    # =====================================
    # Build Intent Response
    # =====================================

    def build_response(
        self,
        intent: str,
        target: Optional[str] = None,
        confidence: float = 1.0,
    ) -> Dict:

        return {
            "intent": intent,
            "target": target,
            "confidence": confidence,
        }

    # =====================================
    # Detect Open Intent
    # =====================================

    def detect_open(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        if not any(keyword in message for keyword in self.open_keywords):
            return None

        for alias in self.application_map:

            if alias in message:

                app = self.normalize_application(alias)

                logger.info(
                    f"Open intent detected -> {app}"
                )

                return self.build_response(
                    intent="open",
                    target=app,
                    confidence=0.98,
                )

        logger.info("Generic open intent detected.")

        return self.build_response(
            intent="open",
            target=None,
            confidence=0.75,
        )

    # =====================================
    # Engine Information
    # =====================================

    def info(self) -> Dict:

        return {
            "engine": self.name,
            "version": "3.0",
            "supported_intents": [
                "open",
            ],
            "supported_applications": sorted(
                list(
                    set(
                        self.application_map.values()
                    )
                )
            ),
        }
    # =====================================
    # Detect Close Intent
    # =====================================

    def detect_close(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        if not any(keyword in message for keyword in self.close_keywords):
            return None

        for alias in self.application_map:

            if alias in message:

                app = self.normalize_application(alias)

                logger.info(
                    f"Close intent detected -> {app}"
                )

                return self.build_response(
                    intent="close",
                    target=app,
                    confidence=0.98,
                )

        logger.info("Generic close intent detected.")

        return self.build_response(
            intent="close",
            target=None,
            confidence=0.75,
        )

    # =====================================
    # Detect Shutdown Intent
    # =====================================

    def detect_shutdown(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        if any(keyword in message for keyword in self.shutdown_keywords):

            logger.info("Shutdown intent detected.")

            return self.build_response(
                intent="shutdown",
                confidence=0.99,
            )

        return None

    # =====================================
    # Detect Restart Intent
    # =====================================

    def detect_restart(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        if any(keyword in message for keyword in self.restart_keywords):

            logger.info("Restart intent detected.")

            return self.build_response(
                intent="restart",
                confidence=0.99,
            )

        return None

    # =====================================
    # Detect Search Intent
    # =====================================

    def detect_search(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        for keyword in self.search_keywords:

            if keyword in message:

                query = message.replace(keyword, "").strip()

                logger.info(
                    f"Search intent detected -> {query}"
                )

                return self.build_response(
                    intent="search",
                    target=query if query else None,
                    confidence=0.95,
                )

        return None

    # =====================================
    # Main Intent Detector
    # =====================================

    def detect(self, message: str) -> Dict:

        detectors = [
            self.detect_open,
            self.detect_close,
            self.detect_shutdown,
            self.detect_restart,
            self.detect_search,
        ]

        for detector in detectors:

            result = detector(message)

            if result is not None:
                return result

        logger.info("Chat intent detected.")

        return self.build_response(
            intent="chat",
            target=message,
            confidence=0.50,
        )
    # -----------------------------
        # Website Keywords
        # -----------------------------

        self.website_keywords = [
            "website",
            "site",
            "web",
            "browser",

            # Roman Urdu
            "website kholo",
            "site kholo",
            "web kholo",
            "browser kholo",
        ]

        # -----------------------------
        # Folder Keywords
        # -----------------------------

        self.folder_keywords = [
            "folder",
            "directory",

            # Roman Urdu
            "folder kholo",
            "folder open karo",
            "directory kholo",
        ]

        # -----------------------------
        # File Keywords
        # -----------------------------

        self.file_keywords = [
            "file",
            "document",
            "pdf",
            "word",
            "excel",
            "powerpoint",
            "text file",

            # Roman Urdu
            "file kholo",
            "document kholo",
            "pdf kholo",
            "word kholo",
            "excel kholo",
        ]
    # =====================================
    # Detect Website Intent
    # =====================================

    def detect_website(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        if not any(keyword in message for keyword in self.website_keywords):
            return None

        words = message.split()

        website = None

        for word in words:

            if "." in word:
                website = word
                break

        logger.info(
            f"Website intent detected -> {website}"
        )

        return self.build_response(
            intent="website",
            target=website,
            confidence=0.95,
        )

    # =====================================
    # Detect Folder Intent
    # =====================================

    def detect_folder(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        if not any(keyword in message for keyword in self.folder_keywords):
            return None

        folder_name = message

        for keyword in self.folder_keywords:
            folder_name = folder_name.replace(keyword, "")

        folder_name = folder_name.strip()

        logger.info(
            f"Folder intent detected -> {folder_name}"
        )

        return self.build_response(
            intent="folder",
            target=folder_name if folder_name else None,
            confidence=0.94,
        )
    # =====================================
    # Detect File Intent
    # =====================================

    def detect_file(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        if not any(keyword in message for keyword in self.file_keywords):
            return None

        file_name = message

        for keyword in self.file_keywords:
            file_name = file_name.replace(keyword, "", 1)

        file_name = file_name.strip()

        logger.info(f"File intent detected -> {file_name}")

        return self.build_response(
            intent="file",
            target=file_name if file_name else None,
            confidence=0.95,
        )

    # =====================================
    # Main Intent Dispatcher
    # =====================================

    def detect(self, message: str) -> Optional[Dict]:

        message = self.normalize_text(message)

        detectors = [
            self.detect_open,
            self.detect_close,
            self.detect_shutdown,
            self.detect_restart,
            self.detect_search,
            self.detect_website,
            self.detect_folder,
            self.detect_file,
        ]

        for detector in detectors:

            result = detector(message)

            if result is not None:
                return result

        return self.build_response(
            intent="unknown",
            target=None,
            confidence=0.0,
        )

    # =====================================
    # Engine Information
    # =====================================

    def info(self) -> Dict:

        return {
            "name": "Sigma Intent Engine",
            "version": "3.0",
            "supported_intents": [
                "open",
                "close",
                "shutdown",
                "restart",
                "search",
                "website",
                "folder",
                "file",
            ]
        }