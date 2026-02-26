import logging
import random
import time

logger = logging.getLogger(__name__)


class MockBinanceFuturesClient:
    """
    Simulates Binance Futures execution.
    Used when USE_MOCK=True.
    """

    def place_market_order(self, symbol: str, side: str, quantity: float):
        logger.info(f"[MOCK] MARKET order | {symbol} | {side} | qty={quantity}")
        time.sleep(1)

        return {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "status": "FILLED",
            "orderId": random.randint(1000000, 9999999),
            "price": "0",
            "origQty": str(quantity),
            "executedQty": str(quantity),
        }

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        logger.info(f"[MOCK] LIMIT order | {symbol} | {side} | qty={quantity} | price={price}")
        time.sleep(1)

        return {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "status": "NEW",
            "orderId": random.randint(1000000, 9999999),
            "price": str(price),
            "origQty": str(quantity),
            "executedQty": "0",
        }