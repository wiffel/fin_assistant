from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    pythonpath: str = Field(..., env="PYTHONPATH")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    alphavantage_api_key: str = Field(..., env="ALPHAVANTAGE_API_KEY")
    langchain_tracing_v2: bool = Field(..., env="LANGCHAIN_TRACING_V2")
    langchain_endpoint: str = Field(..., env="LANGCHAIN_ENDPOINT")
    langchain_api_key: str = Field(..., env="LANGCHAIN_API_KEY")
    langchain_project: str = Field(..., env="LANGCHAIN_PROJECT")
    project_root: Path = PROJECT_ROOT
    assistant_title: str = 'Financial Assistant'

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
