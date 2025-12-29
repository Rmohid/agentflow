"""Application configuration using Pydantic Settings"""

from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "AgentFlow"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    api_workers: int = 1
    
    # Logging
    log_level: str = "INFO"
    json_logs: bool = False
    
    # Task Queue
    max_concurrent_tasks: int = 5
    task_retry_limit: int = 3
    task_timeout_seconds: int = 300
    
    # Agent Configuration
    agent_timeout_seconds: int = 600
    agent_max_retries: int = 3
    
    # Storage
    state_dir: Path = Field(default=Path(".agentflow_state"))
    workspace_dir: Path = Field(default=Path(".agentflow_workspace"))
    
    # GitHub (optional, for GitHub agent)
    github_token: Optional[str] = None
    github_api_url: str = "https://api.github.com"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    
    # CORS
    cors_enabled: bool = True
    cors_origins: list[str] = Field(default=["*"])
    
    def ensure_directories(self) -> None:
        """Ensure required directories exist"""
        self.state_dir.mkdir(exist_ok=True, parents=True)
        self.workspace_dir.mkdir(exist_ok=True, parents=True)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    settings.ensure_directories()
    return settings
