import logging

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    """
    Real Binance Futures Client (Testnet).
    Not used when USE_MOCK=True.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

        logger.info("BinanceFuturesClient initialized (real mode).")

    def place_market_order(self, symbol: str, side: str, quantity: float):
        """
        Placeholder for real Binance market order.
        """
        raise NotImplementedError(
            "Real Binance execution not enabled. Set USE_MOCK=False and implement real client."
        )

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        """
        Placeholder for real Binance limit order.
        """
        raise NotImplementedError(
            "Real Binance execution not enabled. Set USE_MOCK=False and implement real client."
        )