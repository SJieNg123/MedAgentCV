from __future__ import annotations

import tempfile
from typing import Dict

from fastapi import FastAPI, File, Form, UploadFile

from app.schema import AnalysisResponse
from app.workflow.graph import compile_graph

app = FastAPI(title="VinBigData Vision-Language Agent API", version="0.1.0")


@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_image(
	disease_description: str = Form(...),
	image: UploadFile = File(...),
) -> AnalysisResponse:
	with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
		contents = await image.read()
		temp_file.write(contents)
		image_path = temp_file.name

	graph = compile_graph()

	initial_state: Dict[str, object] = {
		"image_path": image_path,
		"disease_description": disease_description,
		"cv_tool_raw_output": "",
		"draft_analysis": "",
		"verification_feedback": "",
		"is_consistent": False,
		"iterations": 0,
		"messages": [],
	}

	final_state = graph.invoke(initial_state)

	return AnalysisResponse(
		final_analysis=final_state.get("draft_analysis", ""),
		is_consistent=bool(final_state.get("is_consistent")),
		iterations=int(final_state.get("iterations", 0)),
		verification_feedback=final_state.get("verification_feedback"),
		cv_tool_raw_output=final_state.get("cv_tool_raw_output"),
		draft_analysis=final_state.get("draft_analysis"),
		messages=[getattr(msg, "content", str(msg)) for msg in final_state.get("messages", [])],
	)
