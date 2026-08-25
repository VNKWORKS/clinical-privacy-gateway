from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClinicalShield Secure PHI Deidentification Gateway"
    environment: str = "development"
    log_level: str = "INFO"

    llm_provider: str = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.5"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()