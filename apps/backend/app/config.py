from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    app_name: str = "Xish AI Backend"
    environment: str = "development"
    debug: bool = True

    # CORS
    cors_origins: list[str] = ["*"]

    # Database
    database_url: SecretStr | None = None

    # Supabase
    supabase_url: str | None = None
    supabase_anon_key: SecretStr | None = None
    supabase_service_role_key: SecretStr | None = None
    supabase_jwks_url: str | None = None

    # AI Providers
    openai_api_key: SecretStr | None = None
    default_model: str = "gpt-4o-mini"

    # Rate Limiting
    rate_limit_per_minute: int = 60

    # Security
    jwt_aud: str | None = None
    jwt_iss: str | None = None

    class Config:
        env_file = ".env"
        env_prefix = "XISH_"


settings = Settings()  # type: ignore[arg-type]
