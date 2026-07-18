from src.core.logger import logger


class AIProvider:

    def __init__(self):

        self.provider = None

        logger.info("AI Provider Initialized")


    def set_provider(self, provider_name):

        self.provider = provider_name

        logger.info(f"Current AI Provider : {provider_name}")


    def get_provider(self):

        return self.provider


    def generate(self, prompt):

        if self.provider is None:

            logger.warning("No AI Provider Selected")

            return None

        logger.info(f"Generating Response using {self.provider}")

        return f"[{self.provider}] Processing: {prompt}"