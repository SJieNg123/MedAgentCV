from __future__ import annotations

from typing import Dict

from langchain_core.messages import AIMessage

from app.config import get_settings
from app.workflow.state import GraphState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def run_verify_agent(state: GraphState) -> Dict[str, object]:
	settings = get_settings()
	llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)

	prompt = ChatPromptTemplate.from_messages(
		[
			(
				"system",
				"You are a strict medical consistency reviewer. "
				"Compare the user's description with the draft analysis. "
				"If consistent, reply with 'CONSISTENT'. "
				"Otherwise, reply with a concise contradiction or hallucination feedback.",
			),
			(
				"human",
				"User description: {description}\nDraft analysis: {draft}",
			),
		]
	)

	response = llm.invoke(
		prompt.format_messages(
			description=state["disease_description"],
			draft=state["draft_analysis"],
		)
	)

	content = response.content.strip()
	is_consistent = content.upper().startswith("CONSISTENT")
	message = AIMessage(content=content)

	return {
		"verification_feedback": content,
		"is_consistent": is_consistent,
		"iterations": state.get("iterations", 0) + 1,
		"messages": state.get("messages", []) + [message],
	}
