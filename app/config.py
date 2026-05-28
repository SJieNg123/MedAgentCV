from __future__ import annotations

import os

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict




class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", extra="ignore")

	openai_api_key: str = os.getenv("OPENAI_API_KEY")
	openai_model: str = os.getenv("OPENAI_MODEL")
	max_iterations: int = int(os.getenv("MAX_ITERATIONS"))

@lru_cache
def get_settings() -> Settings:
	return Settings()
