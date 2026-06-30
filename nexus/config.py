"""
Global application settings using Pydantic.

Reads from environment variables and the .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Core application settings.
    Fields correspond to environment variables defined in .env.example.
    """
    
    # App Settings
    nexus_env: str = "development"
    nexus_log_level: str = "INFO"
    nexus_log_format: str = "console"
    nexus_max_retry_count: int = 3
    nexus_session_timeout_seconds: int = 3600
    
    # LLM Settings
    llm_provider: str = "ollama"
    
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"
    
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    ollama_embedding_model: str = "nomic-embed-text"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore env vars not defined here
    )

# Global settings instance
settings = Settings()
