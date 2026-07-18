from src.core.logger import logger
from src.ai.prompts import SYSTEM_PROMPT
from src.ai.providers import AIProvider


class Brain:

    def __init__(self):

        self.name = "Sigma Brain"
        self.version = "1.0.0"

        self.provider = AIProvider()

        self.system_prompt = SYSTEM_PROMPT

        logger.info(f"{self.name} Loaded Successfully")

    def set_provider(self, provider_name):

        self.provider.set_provider(provider_name)

    def get_provider(self):

        return self.provider.get_provider()

    def build_prompt(self, user_message, memory=None):

        prompt = self.system_prompt

        if memory:

            prompt += "\n\nConversation Memory:\n"
            prompt += str(memory)

        prompt += "\n\nUser:\n"
        prompt += user_message

        return prompt

    def think(self, user_message, memory=None):

        logger.info("=" * 50)
        logger.info("Sigma AI Thinking...")
        logger.info(f"User Message : {user_message}")

        prompt = self.build_prompt(
            user_message=user_message,
            memory=memory
        )

        logger.info("Prompt Created Successfully.")

        response = self.provider.generate(prompt)

        logger.info("Thinking Complete.")
        logger.info(f"Response Generated : {response}")

        return response

    def chat(self, message, memory=None):

        logger.info("=" * 50)
        logger.info(f"User : {message}")

        response = self.think(
            user_message=message,
            memory=memory
        )

        logger.info(f"Assistant : {response}")
        logger.info("=" * 50)

        return response

    def ask(self, message, memory=None):

        """
        Public method used by SigmaAgent.
        """

        return self.chat(
            message=message,
            memory=memory
        )

    def info(self):

        return {
            "name": self.name,
            "version": self.version,
            "provider": self.get_provider()
        }