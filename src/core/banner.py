from datetime import datetime
import platform

from rich.console import Console
from rich.panel import Panel

console = Console()


def show_banner(
    agent_name="Sigma AI Desktop Agent",
    version="1.0.0",
    developer="Sigma",
    ai_engine="OpenAI (Configurable)",
    environment="Development",
):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    banner = f"""
🤖 Agent Name : {agent_name}

📦 Version    : {version}
👨‍💻 Developer : {developer}
🧠 AI Engine  : {ai_engine}
⚙ Environment: {environment}

──────────── SYSTEM STATUS ────────────

🟢 Core Engine      : Ready
🟢 Configuration    : Ready
🟢 Logger           : Ready
🟡 Memory           : Pending
🟡 Browser          : Pending
🟡 Desktop Control  : Pending
🟡 Voice            : Pending
🟡 Vision           : Pending
🟡 WhatsApp         : Pending
🟡 Database         : Pending

──────────── SYSTEM INFO ─────────────

💻 OS      : {platform.system()}
🐍 Python  : {platform.python_version()}
🕒 Started : {current_time}
"""

    console.print(
        Panel.fit(
            banner,
            title="🚀 Sigma AI Desktop Agent",
            border_style="green",
        )
    )


if __name__ == "__main__":
    show_banner()