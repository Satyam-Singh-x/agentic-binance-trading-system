from pydantic import BaseModel, Field
from typing import Optional


class TradingOrderSchema(BaseModel):
    symbol: str = Field(
        description="Trading symbol in uppercase, e.g., BTCUSDT"
    )
    side: str = Field(
        description="BUY or SELL"
    )
    order_type: str = Field(
        description="MARKET or LIMIT"
    )
    quantity: float = Field(
        description="Order quantity as a numeric value"
    )
    price: Optional[float] = Field(
        description="Limit price if order_type is LIMIT, otherwise null"
    )