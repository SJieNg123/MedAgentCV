from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", extra="ignore")

	openai_api_key: str
	openai_model: str = "gpt-4o-mini"
	max_iterations: int = 3


@lru_cache
def get_settings() -> Settings:
	return Settings()
