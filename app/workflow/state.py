from __future__ import annotations

from typing import List, TypedDict

from langchain_core.messages import BaseMessage


class GraphState(TypedDict):
	image_path: str
	disease_description: str
	cv_tool_raw_output: str
	draft_analysis: str
	verification_feedback: str
	is_consistent: bool
	iterations: int
	messages: List[BaseMessage]
