from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    GOOGLE_PLACES_API_KEY: str
    MAPBOX_API_KEY: str

    APP_NAME: str = "NomadIQ"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    ALLOWED_ORIGINS: str = "*"

    @property
    def allowed_origins_list(self):
        if self.ALLOWED_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()