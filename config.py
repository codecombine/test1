from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    TAVILY_API_KEY: str = ""
    DATABASE_URL: str = "weekend_buddy.db"

    model_config = {"env_file": ".env"}


settings = Settings()
