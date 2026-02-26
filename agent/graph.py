from langgraph.graph import StateGraph, END
from agent.state import TradingState
from agent.nodes import (
    parse_node,
    validation_node,
    execution_node,
    summary_node,
)


def build_graph():
    """
    Build and compile the LangGraph workflow.
    """

    workflow = StateGraph(TradingState)

    # Add nodes
    workflow.add_node("parse", parse_node)
    workflow.add_node("validate", validation_node)
    workflow.add_node("execute", execution_node)
    workflow.add_node("summarize", summary_node)

    # Entry point
    workflow.set_entry_point("parse")

    # Flow definition
    workflow.add_edge("parse", "validate")
    workflow.add_edge("validate", "execute")
    workflow.add_edge("execute", "summarize")
    workflow.add_edge("summarize", END)

    return workflow.compile()


def run_agent(user_input: str):
    """
    Execute the trading agent workflow.
    """

    graph = build_graph()

    initial_state = {
        "raw_input": user_input,
        "structured_order": None,
        "validation_error": None,
        "execution_result": None,
        "summary": None,
    }

    final_state = graph.invoke(initial_state)

    return final_state