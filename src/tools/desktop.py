"""
=========================================
 Sigma AI Desktop Controller
 Version : 2.0
=========================================
"""

import os
import subprocess
import webbrowser

from src.core.logger import logger


class DesktopController:

    def __init__(self):

        self.name = "Desktop Controller"

        self.supported_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "explorer": "explorer.exe"
        }

        logger.info(f"{self.name} Loaded Successfully")

    # ------------------------------------
    # Applications
    # ------------------------------------

    def open_application(self, application):

        app = application.lower().strip()

        if app not in self.supported_apps:

            logger.warning(f"Unsupported Application : {application}")

            return False

        try:

            subprocess.Popen(self.supported_apps[app])

            logger.success(f"{application} Opened Successfully")

            return True

        except Exception as error:

            logger.exception(error)

            return False

    # ------------------------------------
    # Files & Folders
    # ------------------------------------

    def open_folder(self, folder_path):

        try:

            os.startfile(folder_path)

            logger.success(f"Folder Opened : {folder_path}")

            return True

        except Exception as error:

            logger.exception(error)

            return False

    def open_file(self, file_path):

        try:

            os.startfile(file_path)

            logger.success(f"File Opened : {file_path}")

            return True

        except Exception as error:

            logger.exception(error)

            return False

    # ------------------------------------
    # Browser
    # ------------------------------------

    def open_url(self, url):

        try:

            webbrowser.open(url)

            logger.success(f"Opened URL : {url}")

            return True

        except Exception as error:

            logger.exception(error)

            return False

    def search_google(self, query):

        url = f"https://www.google.com/search?q={query}"

        return self.open_url(url)

    # ------------------------------------
    # Desktop
    # ------------------------------------

    def show_desktop(self):

        try:

            subprocess.Popen(
                "powershell -command \"(New-Object -ComObject Shell.Application).ToggleDesktop()\"",
                shell=True
            )

            logger.success("Desktop Displayed")

            return True

        except Exception as error:

            logger.exception(error)

            return False

    # ------------------------------------
    # Information
    # ------------------------------------

    def list_supported_apps(self):

        return list(self.supported_apps.keys())

    def is_supported(self, application):

        return application.lower().strip() in self.supported_apps

    def info(self):

        return {
            "name": self.name,
            "supported_apps": self.list_supported_apps()
        }