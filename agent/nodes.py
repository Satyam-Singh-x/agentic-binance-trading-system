import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser

from bot.config import settings
from bot.validators import validate_order, ValidationError
from bot.orders import OrderService
from agent.schema import TradingOrderSchema

logger = logging.getLogger(__name__)

# =========================================================
# ================= LLM INITIALIZATION ====================
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0,
)

parser = PydanticOutputParser(pydantic_object=TradingOrderSchema)

# =========================================================
# ====================== PARSE NODE =======================
# =========================================================

def parse_node(state):
    logger.info("========== PARSE NODE STARTED ==========")

    format_instructions = parser.get_format_instructions()

    prompt = f"""
    You are a deterministic trading instruction parser for a Binance Futures USDT-M system.

    Your ONLY task:
    Convert a user trading instruction into a structured trading order.

    You are NOT allowed to:
    - Provide explanations.
    - Provide commentary.
    - Add extra fields.
    - Invent values.
    - Guess missing required information.
    - Modify quantities or prices.
    - Assume leverage, margin, stop loss, or take profit.

    You must strictly follow the transformation rules below.

    --------------------------------------------------
    REQUIRED OUTPUT FIELDS
    --------------------------------------------------
    symbol: string
    side: BUY or SELL
    order_type: MARKET or LIMIT
    quantity: numeric
    price: numeric or null

    No additional fields are allowed.

    --------------------------------------------------
    SYMBOL RULES
    --------------------------------------------------
    - Convert BTC → BTCUSDT
    - Convert ETH → ETHUSDT
    - If only base asset provided → default to USDT pair
    - Keep symbol uppercase
    - Do NOT invent unsupported symbols
    - If symbol cannot be determined → fail parsing

    --------------------------------------------------
    SIDE RULES
    --------------------------------------------------
    - "long" → BUY
    - "buy" → BUY
    - "short" → SELL
    - "sell" → SELL
    - Only BUY or SELL allowed
    - If side not clearly stated → fail parsing

    --------------------------------------------------
    ORDER TYPE RULES
    --------------------------------------------------
    - If explicit price is mentioned → LIMIT
    - If no price mentioned → MARKET
    - Only MARKET or LIMIT allowed

    --------------------------------------------------
    QUANTITY RULES
    --------------------------------------------------
    - Extract the exact numeric quantity mentioned
    - Do NOT infer or calculate quantity
    - If quantity missing → fail parsing

    --------------------------------------------------
    PRICE RULES
    --------------------------------------------------
    - For MARKET orders → price must be null
    - For LIMIT orders → extract numeric price
    - If LIMIT but price missing → fail parsing

    --------------------------------------------------
    FAILURE RULE
    --------------------------------------------------
    If ANY required field (symbol, side, quantity, order_type) 
    cannot be confidently determined:
    Return a parsing failure according to the output schema.
    Do NOT guess.

    --------------------------------------------------
    EXAMPLES
    --------------------------------------------------

    Example 1:
    Input: "Buy 0.01 BTC at market"

    Expected Output:
    symbol: BTCUSDT
    side: BUY
    order_type: MARKET
    quantity: 0.01
    price: null

    Example 2:
    Input: "Short 0.5 ETH at 2800"

    Expected Output:
    symbol: ETHUSDT
    side: SELL
    order_type: LIMIT
    quantity: 0.5
    price: 2800

    Example 3 (Invalid Case):
    Input: "Buy BTC"

    Reason:
    Quantity missing → parsing must fail.

    --------------------------------------------------

    You MUST strictly follow the schema format below:

    {format_instructions}

    Now parse this instruction:
    {state['raw_input']}
    """.strip()



    try:
        logger.info(f"[PARSE] Raw Input: {state['raw_input']}")

        response = llm.invoke(prompt)

        if not response.content:
            raise ValueError("Empty LLM response.")

        logger.info("[PARSE] LLM response received. Parsing structured output...")

        structured_response = parser.parse(response.content.strip())
        order_dict = structured_response.model_dump()

        state["structured_order"] = order_dict
        state["validation_error"] = None

        logger.info(f"[PARSE] Parsing successful: {order_dict}")

    except Exception as e:
        state["validation_error"] = f"Parsing failed: {str(e)}"
        logger.error("[PARSE] Parsing failed.", exc_info=True)

    logger.info("========== PARSE NODE COMPLETED ==========")

    return state


# =========================================================
# =================== VALIDATION NODE =====================
# =========================================================

def validation_node(state):
    logger.info("========== VALIDATION NODE STARTED ==========")

    if state.get("validation_error"):
        logger.warning("[VALIDATION] Skipped due to previous error.")
        logger.info("========== VALIDATION NODE COMPLETED ==========")
        return state

    try:
        order = state["structured_order"]
        logger.info(f"[VALIDATION] Validating order: {order}")

        validate_order(
            symbol=order["symbol"],
            side=order["side"],
            order_type=order["order_type"],
            quantity=order["quantity"],
            price=order.get("price"),
        )

        state["validation_error"] = None
        logger.info("[VALIDATION] Validation successful.")

    except ValidationError as ve:
        state["validation_error"] = str(ve)
        logger.warning(f"[VALIDATION] Validation failed: {ve}")

    except Exception:
        state["validation_error"] = "Validation failed."
        logger.error("[VALIDATION] Unexpected validation error.", exc_info=True)

    logger.info("========== VALIDATION NODE COMPLETED ==========")

    return state


# =========================================================
# ==================== EXECUTION NODE =====================
# =========================================================

def execution_node(state):
    logger.info("========== EXECUTION NODE STARTED ==========")

    if state.get("validation_error"):
        logger.warning("[EXECUTION] Skipped due to validation error.")
        logger.info("========== EXECUTION NODE COMPLETED ==========")
        return state

    service = OrderService()
    order = state["structured_order"]

    try:
        logger.info(f"[EXECUTION] Executing order: {order}")

        result = service.execute_order(
            symbol=order["symbol"],
            side=order["side"],
            order_type=order["order_type"],
            quantity=order["quantity"],
            price=order.get("price"),
        )

        state["execution_result"] = result

        logger.info(
            f"[EXECUTION] Success | Order ID: {result.get('orderId')} | "
            f"Status: {result.get('status')}"
        )

    except Exception as e:
        state["validation_error"] = str(e)
        logger.error("[EXECUTION] Execution failed.", exc_info=True)

    logger.info("========== EXECUTION NODE COMPLETED ==========")

    return state


# =========================================================
# ===================== SUMMARY NODE ======================
# =========================================================

def summary_node(state):
    logger.info("========== SUMMARY NODE STARTED ==========")

    if state.get("validation_error"):
        logger.warning("[SUMMARY] Generating error summary.")
        state["summary"] = f"❌ Error: {state['validation_error']}"
        logger.info("========== SUMMARY NODE COMPLETED ==========")
        return state

    result = state.get("execution_result")

    if not result:
        logger.warning("[SUMMARY] No execution result found.")
        state["summary"] = "No execution result available."
        logger.info("========== SUMMARY NODE COMPLETED ==========")
        return state

    prompt = f"""
You are a professional trading execution analyst for a Binance Futures trading system.

Generate a concise, factual explanation of the executed trade.

Rules:
- No trading advice.
- No speculation.
- Only use provided execution data.
- 4–6 sentences maximum.

Execution Data:
{result}
""".strip()

    try:
        logger.info("[SUMMARY] Generating execution summary via LLM.")

        response = llm.invoke(prompt)

        state["summary"] = response.content
        logger.info("[SUMMARY] Summary generation successful.")

    except Exception:
        logger.error("[SUMMARY] Summary generation failed.", exc_info=True)
        state["summary"] = "Summary generation failed."

    logger.info("========== SUMMARY NODE COMPLETED ==========")

    return state