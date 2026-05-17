from __future__ import annotations

from langchain_core.tools import tool


@tool("mock_vinbigdata_cv")
def mock_vinbigdata_cv(image_path: str) -> str:
	"""Mock VinBigData CV extraction for chest X-ray abnormalities."""
	return (
		"Findings from image at "
		f"{image_path}: Cardiomegaly (0.87), Pleural effusion (0.78), "
		"Atelectasis (0.64), No pneumothorax (0.92)."
	)
