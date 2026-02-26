from bot.logging_config import setup_logging
from bot.orders import OrderService

setup_logging()

service = OrderService()

result = service.execute_order(
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity=0.01,
)

print(result)