from __future__ import annotations

from typing import Literal

from langgraph.graph import END, StateGraph

from app.config import get_settings
from app.workflow.agents.analytic import run_analytic_agent
from app.workflow.agents.verify import run_verify_agent
from app.workflow.state import GraphState


def _route_after_verify(state: GraphState) -> Literal["analytic", "end"]:
	settings = get_settings()
	if state.get("is_consistent"):
		return "end"
	if state.get("iterations", 0) >= settings.max_iterations:
		return "end"
	return "analytic"


def build_graph() -> StateGraph:
	graph = StateGraph(GraphState)
	graph.add_node("analytic", run_analytic_agent)
	graph.add_node("verify", run_verify_agent)
	graph.set_entry_point("analytic")
	graph.add_edge("analytic", "verify")
	graph.add_conditional_edges(
		"verify",
		_route_after_verify,
		{
			"analytic": "analytic",
			"end": END,
		},
	)
	return graph


def compile_graph():
	return build_graph().compile()
