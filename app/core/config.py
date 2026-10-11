from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Secure Enterprise AI"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    max_document_chars: int = 100_000
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
