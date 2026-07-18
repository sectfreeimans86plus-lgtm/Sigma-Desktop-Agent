"""
=========================================
Sigma AI - Intent Engine
Version : 3.1
=========================================
"""

import re
import unicodedata
from typing import Any, Callable, Dict, Final, List, Optional

from src.core.logger import logger

IntentResult = Dict[str, Any]
Detector = Callable[[str], Optional[IntentResult]]


class IntentEngine:
    """
    Sigma Intent Detection Engine.

    Converts natural-language user input (English and Roman Urdu) into
    structured intent payloads for SigmaAgent and DesktopController.
    """

    ENGINE_NAME: Final[str] = "Sigma Intent Engine"
    ENGINE_VERSION: Final[str] = "3.1"

    _URL_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?"
        r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
        r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+"
        r"(?:/[^\s]*)?",
        re.IGNORECASE,
    )

    _SYSTEM_CONTEXT_WORDS = frozenset(
        {
            "system",
            "computer",
            "pc",
            "laptop",
            "machine",
            "windows",
        }
    )

    def __init__(self) -> None:
        self.name = self.ENGINE_NAME

        self.open_keywords = self._sort_keywords(
            [
                "open up",
                "open",
                "launch",
                "start",
                "run",
                "execute",
                "khol do",
                "chala do",
                "start karo",
                "run karo",
                "khol",
                "kholo",
                "chalao",
            ]
        )

        self.close_keywords = self._sort_keywords(
            [
                "close down",
                "close",
                "exit",
                "quit",
                "terminate",
                "kill",
                "stop",
                "band kar do",
                "band karo",
                "close karo",
                "exit karo",
                "quit karo",
            ]
        )

        self.shutdown_keywords = self._sort_keywords(
            [
                "shut down",
                "shutdown",
                "power off",
                "turn off",
                "system shutdown",
                "computer shutdown",
                "pc shutdown",
                "laptop shutdown",
                "system band karo",
            ]
        )

        self.restart_keywords = self._sort_keywords(
            [
                "re boot",
                "reboot",
                "restart",
                "system restart",
                "computer restart",
                "pc restart",
                "restart karo",
                "reboot karo",
            ]
        )

        self.search_keywords = self._sort_keywords(
            [
                "search google for",
                "google search for",
                "search for",
                "look up",
                "lookup",
                "find on google",
                "search on google",
                "google search",
                "search",
                "dhundho",
                "dhundo",
                "talash karo",
            ]
        )

        self.website_keywords = self._sort_keywords(
            [
                "navigate to",
                "go to",
                "visit",
                "browse",
                "open website",
                "open site",
                "open web",
                "website kholo",
                "site kholo",
                "web kholo",
                "web page",
                "webpage",
                "website",
                "site",
            ]
        )

        self.folder_keywords = self._sort_keywords(
            [
                "open folder",
                "folder open karo",
                "folder kholo",
                "directory kholo",
                "folder",
                "directory",
            ]
        )

        self.file_keywords = self._sort_keywords(
            [
                "open file",
                "text file",
                "file kholo",
                "document kholo",
                "pdf kholo",
                "word kholo",
                "excel kholo",
                "powerpoint",
                "document",
                "pdf",
                "excel",
                "word",
                "file",
            ]
        )

        self.application_map: Dict[str, str] = {
            "google chrome": "chrome",
            "microsoft edge": "edge",
            "visual studio code": "vscode",
            "file explorer": "explorer",
            "command prompt": "cmd",
            "notepad++": "notepad",
            "vs code": "vscode",
            "mspaint": "paint",
            "browser": "chrome",
            "chrome": "chrome",
            "edge": "edge",
            "firefox": "firefox",
            "notepad": "notepad",
            "vscode": "vscode",
            "calculator": "calculator",
            "calc": "calculator",
            "paint": "paint",
            "cmd": "cmd",
            "powershell": "powershell",
            "explorer": "explorer",
        }

        self._application_aliases = self._sort_keywords(
            list(self.application_map.keys())
        )

        self._detectors: List[Detector] = [
            self.detect_shutdown,
            self.detect_restart,
            self.detect_close,
            self.detect_search,
            self.detect_website,
            self.detect_file,
            self.detect_folder,
            self.detect_open,
        ]

        logger.info(f"{self.name} initialized successfully.")

    @staticmethod
    def _sort_keywords(keywords: List[str]) -> List[str]:
        unique = list(
            dict.fromkeys(keyword.strip().lower() for keyword in keywords if keyword.strip())
        )
        return sorted(unique, key=len, reverse=True)

    @staticmethod
    def _clamp_confidence(confidence: float) -> float:
        return round(max(0.0, min(confidence, 1.0)), 2)

    def normalize_text(self, text: str) -> str:
        if not text:
            return ""

        normalized = unicodedata.normalize("NFKC", str(text))
        normalized = normalized.lower().strip()
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized

    def normalize_application(self, app: str) -> Optional[str]:
        if not app:
            return None
        return self.application_map.get(self.normalize_text(app))

    def build_response(
        self,
        intent: str,
        target: Optional[str] = None,
        confidence: float = 1.0,
    ) -> IntentResult:
        return {
            "intent": intent,
            "target": target,
            "confidence": self._clamp_confidence(confidence),
        }

    def _contains_keyword(self, message: str, keywords: List[str]) -> bool:
        return any(self._contains_phrase(message, keyword) for keyword in keywords)

    def _contains_phrase(self, message: str, phrase: str) -> bool:
        if not message or not phrase:
            return False

        if " " in phrase:
            return phrase in message

        pattern = rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])"
        return re.search(pattern, message) is not None

    def _find_matched_keyword(self, message: str, keywords: List[str]) -> Optional[str]:
        for keyword in keywords:
            if self._contains_phrase(message, keyword):
                return keyword
        return None

    def _strip_keywords(
        self,
        message: str,
        keyword_groups: List[List[str]],
    ) -> str:
        result = message

        for keywords in keyword_groups:
            for keyword in keywords:
                if " " in keyword:
                    result = result.replace(keyword, " ")
                else:
                    result = re.sub(
                        rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])",
                        " ",
                        result,
                    )

        result = re.sub(r"\s+", " ", result).strip(" ,.;:-")
        return result

    def _find_application_in_message(self, message: str) -> Optional[str]:
        for alias in self._application_aliases:
            if self._contains_phrase(message, alias):
                return self.application_map[alias]
        return None

    def _has_system_context(self, message: str) -> bool:
        tokens = set(message.split())
        return bool(tokens.intersection(self._SYSTEM_CONTEXT_WORDS))

    def _extract_url(self, message: str) -> Optional[str]:
        match = self._URL_PATTERN.search(message)
        if not match:
            return None

        url = match.group(0).rstrip(".,);]")
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        return url

    def _extract_target_after_keywords(
        self,
        message: str,
        action_keywords: List[str],
        type_keywords: Optional[List[str]] = None,
    ) -> Optional[str]:
        groups = [action_keywords]
        if type_keywords:
            groups.append(type_keywords)

        target = self._strip_keywords(message, groups)
        return target or None

    def detect_open(self, message: str) -> Optional[IntentResult]:
        message = self.normalize_text(message)
        if not message:
            return None

        if not self._contains_keyword(message, self.open_keywords):
            return None

        url = self._extract_url(message)
        if url:
            logger.info(f"Open intent detected (url) -> {url}")
            return self.build_response("open", url, 0.96)

        app = self._find_application_in_message(message)
        if app:
            logger.info(f"Open intent detected -> {app}")
            return self.build_response("open", app, 0.98)

        target = self._extract_target_after_keywords(message, self.open_keywords)
        logger.info("Generic open intent detected.")
        return self.build_response("open", target, 0.75 if target else 0.70)

    def detect_close(self, message: str) -> Optional[IntentResult]:
        message = self.normalize_text(message)
        if not message:
            return None

        if not self._contains_keyword(message, self.close_keywords):
            return None

        app = self._find_application_in_message(message)
        if app:
            logger.info(f"Close intent detected -> {app}")
            return self.build_response("close", app, 0.98)

        target = self._extract_target_after_keywords(message, self.close_keywords)
        logger.info("Generic close intent detected.")
        return self.build_response("close", target, 0.75 if target else 0.70)

    def detect_shutdown(self, message: str) -> Optional[IntentResult]:
        message = self.normalize_text(message)
        if not message:
            return None

        matched = self._find_matched_keyword(message, self.shutdown_keywords)
        if not matched:
            return None

        confidence = 0.99
        if matched in {"turn off", "power off"} and not self._has_system_context(message):
            confidence = 0.82

        logger.info("Shutdown intent detected.")
        return self.build_response("shutdown", None, confidence)

    def detect_restart(self, message: str) -> Optional[IntentResult]:
        message = self.normalize_text(message)
        if not message:
            return None

        if not self._contains_keyword(message, self.restart_keywords):
            return None

        logger.info("Restart intent detected.")
        return self.build_response("restart", None, 0.99)

    def detect_search(self, message: str) -> Optional[IntentResult]:
        message = self.normalize_text(message)
        if not message:
            return None

        matched_keyword = self._find_matched_keyword(message, self.search_keywords)
        if not matched_keyword:
            return None

        query = message.replace(matched_keyword, " ", 1)
        query = re.sub(r"\s+", " ", query).strip(" ,.;:-")

        if not query:
            query = self._strip_keywords(
                message,
                [self.open_keywords, self.close_keywords],
            )

        logger.info(f"Search intent detected -> {query or None}")
        return self.build_response("search", query or None, 0.95 if query else 0.80)

    def detect_website(self, message: str) -> Optional[IntentResult]:
        message = self.normalize_text(message)
        if not message:
            return None

        url = self._extract_url(message)
        has_website_keyword = self._contains_keyword(message, self.website_keywords)

        if url:
            confidence = 0.98 if has_website_keyword else 0.93
            logger.info(f"Website intent detected -> {url}")
            return self.build_response("website", url, confidence)

        if not has_website_keyword:
            return None

        target = self._extract_target_after_keywords(message, self.website_keywords)
        logger.info(f"Website intent detected -> {target or None}")
        return self.build_response("website", target, 0.90 if target else 0.75)

    def detect_folder(self, message: str) -> Optional[IntentResult]:
        message = self.normalize_text(message)
        if not message:
            return None

        if not self._contains_keyword(message, self.folder_keywords):
            return None

        folder_name = self._extract_target_after_keywords(
            message,
            self.open_keywords,
            self.folder_keywords,
        )

        logger.info(f"Folder intent detected -> {folder_name or None}")
        return self.build_response("folder", folder_name, 0.94 if folder_name else 0.78)

    def detect_file(self, message: str) -> Optional[IntentResult]:
        message = self.normalize_text(message)
        if not message:
            return None

        if not self._contains_keyword(message, self.file_keywords):
            return None

        file_name = self._extract_target_after_keywords(
            message,
            self.open_keywords,
            self.file_keywords,
        )

        logger.info(f"File intent detected -> {file_name or None}")
        return self.build_response("file", file_name, 0.95 if file_name else 0.78)

    def detect(self, message: str) -> IntentResult:
        normalized_message = self.normalize_text(message)

        if not normalized_message:
            logger.info("Empty message received; defaulting to chat intent.")
            return self.build_response("chat", None, 0.0)

        for detector in self._detectors:
            result = detector(normalized_message)
            if result is not None:
                return result

        logger.info("Chat intent detected.")
        return self.build_response("chat", normalized_message, 0.50)

    def info(self) -> Dict[str, Any]:
        supported_applications = sorted(set(self.application_map.values()))
        supported_intents = [
            "open",
            "close",
            "shutdown",
            "restart",
            "search",
            "website",
            "folder",
            "file",
            "chat",
        ]

        return {
            "engine": self.name,
            "name": self.name,
            "version": self.ENGINE_VERSION,
            "supported_intents": supported_intents,
            "supported_applications": supported_applications,
        }