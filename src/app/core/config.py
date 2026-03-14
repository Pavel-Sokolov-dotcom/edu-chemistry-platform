from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
    DATABASE_URL: str
    SECRET_KEY: str  # 03ZrF*********************************
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # class Config:
    #     env_file = ".env"


settings = Settings()
