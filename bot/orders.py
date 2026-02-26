import logging
from typing import Optional, Dict, Any

from bot.config import settings
from bot.validators import validate_order, ValidationError
from bot.client import BinanceFuturesClient
from bot.mock_client import MockBinanceFuturesClient

logger = logging.getLogger(__name__)


class OrderService:
    """
    Business logic layer for order execution.
    Handles validation and client selection.
    """

    def __init__(self):
        if settings.USE_MOCK:
            logger.info("Using Mock Binance Client.")
            self.client = MockBinanceFuturesClient()
        else:
            logger.info("Using Real Binance Client.")
            self.client = BinanceFuturesClient(
                api_key=settings.BINANCE_API_KEY,
                api_secret=settings.BINANCE_SECRET_KEY,
                base_url=settings.BINANCE_BASE_URL,
            )

    def execute_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Execute an order after validation.
        """

        try:
            # Normalize inputs
            symbol = symbol.upper()
            side = side.upper()
            order_type = order_type.upper()

            logger.info(
                f"Executing order | {symbol} | {side} | {order_type} | qty={quantity} | price={price}"
            )

            # Validate
            validate_order(symbol, side, order_type, quantity, price)

            # Execute based on order type
            if order_type == "MARKET":
                response = self.client.place_market_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                )

            elif order_type == "LIMIT":
                response = self.client.place_limit_order(
                    symbol=symbol,
                    side=side,
                    quantity=quantity,
                    price=price,
                )

            else:
                raise ValidationError(f"Unsupported order type: {order_type}")

            logger.info(f"Order executed successfully | Order ID: {response.get('orderId')}")

            return self._format_response(response)

        except ValidationError as ve:
            logger.warning(f"Validation failed: {str(ve)}")
            raise

        except Exception as e:
            logger.error("Order execution failed.", exc_info=True)
            raise

    def _format_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and structure response for UI or CLI.
        """

        return {
            "orderId": response.get("orderId"),
            "symbol": response.get("symbol"),
            "side": response.get("side"),
            "type": response.get("type"),
            "status": response.get("status"),
            "price": response.get("price"),
            "origQty": response.get("origQty"),
            "executedQty": response.get("executedQty"),
            "raw": response,
        }

