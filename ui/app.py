import streamlit as st
import logging

from bot.logging_config import setup_logging
from bot.orders import OrderService
from agent.graph import run_agent
from bot.validators import ValidationError

# -------------------------------------------------------
# Setup
# -------------------------------------------------------

setup_logging()
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Agentic Trading System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# Custom CSS Styling
# -------------------------------------------------------

st.markdown("""
<style>

/* Import Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f1b2d;
    padding: 2rem 1.5rem;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Main background */
.main {
    background-color: #eef2f5;
}

/* Headers */
h1 {
    font-weight: 700;
    letter-spacing: -0.5px;
}

/* Buttons */
.stButton>button {
    background-color: #1e8449;
    color: white;
    border-radius: 8px;
    height: 45px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    background-color: #145a32;
}

/* Cards */
.block-container {
    padding-top: 2rem;
}

/* Tabs */
div[data-baseweb="tab"] {
    font-weight: 600;
}

/* JSON box */
.stJson {
    background-color: white !important;
    border-radius: 10px;
    padding: 10px;
}

/* Alerts */
div.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Sidebar Layout
# -------------------------------------------------------

st.sidebar.markdown("## 🚀 Agentic Trading System")
st.sidebar.markdown(
    "Execute Binance Futures trades using either structured inputs or AI-powered natural language."
)

mode = st.sidebar.radio(
    "Select Mode",
    ["Manual Order", "Natural Language"]
)

st.sidebar.markdown("---")

# -------------------------------------------------------
# Main Header Section
# -------------------------------------------------------

st.markdown("""
<div style="padding-bottom: 1rem;">
    <h1>📈 Agentic Binance Futures Execution Engine</h1>
    <p style="color: #555;">Multi-Agent Trading Workflow powered by Gemini + LangGraph</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🧾 Trade", "📜 Execution Logs"])

# =======================================================
# ======================= TRADE TAB ======================
# =======================================================

with tab1:

    if mode == "Manual Order":

        st.subheader("Manual Trade Execution")

        col1, col2 = st.columns(2)

        with col1:
            symbol = st.text_input("Symbol", "BTCUSDT")
            side = st.selectbox("Side", ["BUY", "SELL"])
            quantity = st.number_input("Quantity", min_value=0.0, step=0.01)

        with col2:
            order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
            price = None
            if order_type == "LIMIT":
                price = st.number_input("Price", min_value=0.0, step=0.1)

        if st.button("🚀 Execute Order"):

            try:
                service = OrderService()

                with st.spinner("Executing trade..."):
                    result = service.execute_order(
                        symbol=symbol,
                        side=side,
                        order_type=order_type,
                        quantity=quantity,
                        price=price,
                    )

                st.success("Order Executed Successfully")

                st.markdown("### 📊 Execution Result")
                st.json(result)

            except ValidationError as ve:
                st.error(f"Validation Error: {ve}")

            except Exception as e:
                st.error(f"Execution Error: {e}")

    # ===================================================
    # ============ NATURAL LANGUAGE MODE ================
    # ===================================================

    else:

        st.subheader("AI Agent Trade Execution")

        user_input = st.text_area(
            "Describe your trade instruction",
            placeholder="Example: Buy 0.01 BTC at market"
        )

        if st.button("🤖 Execute via Agent"):

            if not user_input.strip():
                st.warning("Please enter a trading instruction.")
            else:
                with st.spinner("Agent processing..."):
                    result = run_agent(user_input)

                if result["validation_error"]:
                    st.error(result["validation_error"])
                else:
                    st.success("Order Executed Successfully")

                    colA, colB = st.columns(2)

                    with colA:
                        st.markdown("### 🧠 Parsed Order")
                        st.json(result["structured_order"])

                    with colB:
                        st.markdown("### 📦 Execution Data")
                        st.json(result["execution_result"])

                    st.markdown("### 📘 Agent Explanation")
                    st.info(result["summary"])

# =======================================================
# ======================= LOGS TAB ======================
# =======================================================

with tab2:

    st.subheader("Application Logs")

    try:
        with open("logs/trading.log", "r") as f:
            logs = f.readlines()

        last_logs = logs[-80:]

        st.text("".join(last_logs))

    except FileNotFoundError:
        st.warning("Log file not found.")