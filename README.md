🚀 Agentic Binance Futures Trading System


A production-structured, multi-agent crypto trading execution engine built using:

Python

LangGraph

Google Gemini

Streamlit

Modular Backend Architecture

This project supports both CLI-based trading and AI-powered natural language trading, with full validation, logging, and execution abstraction.



📌 Features

✅ Order Execution

MARKET orders

LIMIT orders

BUY / SELL support

Mock execution mode (safe testing)


✅ Multi-Agent Workflow (LangGraph)

Parsing Node (Schema-bound via Pydantic)

Validation Node

Execution Node

Summary Node (LLM-generated explanation)


✅ Dual Interface

Command Line Interface (CLI)

Modern Streamlit Web Dashboard


✅ Clean Architecture

Separation of concerns

Centralized configuration

Structured validation

Rotating log system

Mock & real client abstraction

🏗 Project Structure

Trading_application/

│

├── bot/

│   ├── client.py

│   ├── mock_client.py

│   ├── orders.py

│   ├── validators.py

│   ├── logging_config.py

│   └── config.py
│
├── agent/

│   ├── schema.py

│   ├── state.py

│   ├── nodes.py

│   └── graph.py
│
├── ui/

│   └── app.py

│
├── cli.py

├── requirements.txt

└── README.md


⚙️ Installation

1️⃣ Clone the Repository

git clone https://github.com/Satyam-Singh-x/agentic-binance-trading-system.git

cd agentic-binance-trading-system


2️⃣ Create Virtual Environment

python -m venv venv

source venv/bin/activate  # Mac/Linux

venv\Scripts\activate     # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Create .env File

GOOGLE_API_KEY=your_gemini_api_key

USE_MOCK=True


⚠ Default mode is mock execution for safety.


🖥 CLI Usage

🔹 Market Order

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

🔹 Limit Order

python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 45000



CLI Output Includes:

Order request summary

Execution result

Clear success/failure messages


🌐 Streamlit UI

Run:

streamlit run ui/app.py

Features:

Manual order placement

Natural language trading via Gemini

Execution logs viewer

Structured output display

Clean SaaS-style interface


🤖 Natural Language Examples


You can enter instructions like:


Buy 0.01 BTC at market

Short 0.5 ETH at 2800

Sell 0.2 BTC

The agent will:

Parse instruction using schema validation

Validate order inputs

Execute via mock client

Generate professional execution summary

🧠 Agent Workflow

User Input

   ↓
   
Parse Node (LLM + Pydantic Schema)

   ↓
   
Validation Node

   ↓
   
Execution Node

   ↓
   
Summary Node

   ↓
   
Final Response


This ensures deterministic behavior and reduces hallucination.

📊 Logging

All activity is logged using a rotating file handler:

logs/trading.log

Each node logs:

Start

Success

Errors

Execution details

🔒 Mock Mode

By default:

USE_MOCK=True

This ensures:

No real Binance interaction

Safe simulation

Suitable for development and testing

To enable real trading (future extension):

Add Binance API keys

Set USE_MOCK=False

🛠 Technologies Used

Python 3.10+

LangGraph

Google Gemini (LLM)

Pydantic

Streamlit

Argparse

Logging (RotatingFileHandler)

📈 What Makes This Project Strong

Modular architecture

Clean separation of logic

Schema-enforced LLM parsing

Deterministic workflow

Dual interfaces (CLI + Web)

Production-style logging

Mock-safe execution layer

This is not a script — it is a structured trading execution engine.

🚀 Future Improvements

Risk management node

Position sizing guardrails

Confirmation before execution

Real Binance integration

Docker deployment

Authentication layer

Webhook support

📄 License

This project is developed for technical assessment and educational purposes.

👨‍💻 Author

Satyam Singh

AI / ML Engineer

Specializing in Agentic Systems & Applied LLM Workflows
