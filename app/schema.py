from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
	disease_description: str = Field(..., min_length=3, max_length=500)

class AnalysisResponse(BaseModel):
	final_analysis: str
	is_consistent: bool
	iterations: int
	verification_feedback: Optional[str]
	cv_tool_raw_output: Optional[str]
	draft_analysis: Optional[str]
	messages: List[str] = Field(default_factory=list)
