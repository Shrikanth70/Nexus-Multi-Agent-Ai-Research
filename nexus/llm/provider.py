"""
LLM Provider Factory.

Abstracts the instantiation of LangChain ChatModels so agents do not need to
worry about whether we are using Ollama, OpenAI, or Anthropic.
Reads configuration from nexus/config.py.
"""

from typing import Any
import structlog

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

from nexus.config import settings

logger = structlog.get_logger(__name__)

def get_llm() -> BaseChatModel:
    """
    Factory function to get the configured LLM.
    
    Returns:
        A LangChain BaseChatModel instance.
        
    Raises:
        ValueError: If an unsupported LLM provider is specified in the config.
    """
    provider = settings.llm_provider.lower()
    
    logger.info("Initializing LLM provider", provider=provider)
    
    if provider == "ollama":
        # Ollama requires no API key for local execution.
        return ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0.0, # Deterministic outputs preferred for agents
        )
        
    elif provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when llm_provider is 'openai'")
            
        return ChatOpenAI(
            api_key=settings.openai_api_key, # type: ignore
            model=settings.openai_model,
            temperature=0.0,
        )
        
    elif provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when llm_provider is 'anthropic'")
            
        return ChatAnthropic(
            api_key=settings.anthropic_api_key, # type: ignore
            model_name=settings.anthropic_model,
            temperature=0.0,
        )
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
