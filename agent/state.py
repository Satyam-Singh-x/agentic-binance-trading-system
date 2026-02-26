from typing import TypedDict, Optional, Dict, Any


class TradingState(TypedDict):
    raw_input: str
    structured_order: Optional[Dict[str, Any]]
    validation_error: Optional[str]
    execution_result: Optional[Dict[str, Any]]
    summary: Optional[str]