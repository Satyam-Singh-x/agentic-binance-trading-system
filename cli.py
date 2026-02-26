import argparse
import logging

from bot.logging_config import setup_logging
from bot.orders import OrderService
from bot.validators import validate_order, ValidationError


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description="Binance Futures Trading CLI"
    )

    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price (required for LIMIT)")

    args = parser.parse_args()

    symbol = args.symbol.upper()
    side = args.side.upper()
    order_type = args.type.upper()
    quantity = args.quantity
    price = args.price

    print("\n========== ORDER REQUEST ==========")
    print(f"Symbol     : {symbol}")
    print(f"Side       : {side}")
    print(f"Order Type : {order_type}")
    print(f"Quantity   : {quantity}")
    print(f"Price      : {price}")
    print("===================================\n")

    try:
        validate_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        service = OrderService()

        result = service.execute_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        print(" Order Executed Successfully")
        print("\n========== ORDER RESPONSE ==========")
        print(f"Order ID     : {result.get('orderId')}")
        print(f"Status       : {result.get('status')}")
        print(f"Executed Qty : {result.get('executedQty')}")
        print(f"Avg Price    : {result.get('price')}")
        print("=====================================\n")

        logger.info("CLI order executed successfully.")

    except ValidationError as ve:
        print(f" Validation Error: {ve}")
        logger.warning(f"Validation error: {ve}")

    except Exception as e:
        print(f" Execution Error: {e}")
        logger.error("Execution failed.", exc_info=True)


if __name__ == "__main__":
    main()