import os
from dotenv import load_dotenv


class Settings:
    """
    Central configuration class.
    Loads environment variables and defines global app settings.
    """

    def __init__(self):
        load_dotenv()

        # ===============================
        # === Gemini / LLM Settings ===
        # ===============================
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

        # ===============================
        # === Execution Mode Toggle ===
        # ===============================
        # True → Use mock client
        # False → Use real Binance client
        self.USE_MOCK = os.getenv("USE_MOCK", "True") == "True"

        # ===============================
        # === Binance (Future Ready) ===
        # ===============================
        self.BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
        self.BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
        self.BINANCE_BASE_URL = "https://testnet.binancefuture.com"

        # ===============================
        # === Logging ===
        # ===============================
        self.LOG_FILE = "logs/trading.log"
        self.LOG_LEVEL = "INFO"

        self._validate()

    def _validate(self):
        """
        Validate required configuration.
        """
        if not self.GOOGLE_API_KEY:
            raise EnvironmentError("GOOGLE_API_KEY is required in .env file.")


# Singleton instance
settings = Settings()