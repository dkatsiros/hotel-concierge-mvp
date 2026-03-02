from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://concierge:concierge@db:5432/concierge"
    anthropic_api_key: str = ""
    elevenlabs_api_key: str = ""
    elevenlabs_agent_id: str = ""
    elevenlabs_kb_usage_mode: str = "prompt"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
