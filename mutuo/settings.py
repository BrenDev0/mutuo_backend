from pydantic_settings import BaseSettings
from typing import List
from cryptography.fernet import Fernet


class Settings(BaseSettings):
    ALLOW_ORIGINS: List[str] = ["http://localhost:8000"]

    ENV: str = "local"
    DEBUG: bool = True


    SESSION_MAX_AGE: int = 60 * 60 * 24 * 3 # days default
    USER_CACHE_MAX_AGE: int = 60 * 5
    MAX_VERIFICATION_ATTEMPTS: int = 3
    MAX_LOGIN_ATTEMPS: int = 5

    RATELIMIT: int = 50
    RATE_LIMIT_WINDOW: int = 60

    REDIS_URL: str
    DATABASE_URL: str

    ENCRYPTION_KEY: str = Fernet.generate_key().decode()
    HMAC_KEY: str = Fernet.generate_key().decode()

    class Config:
        env_file = ".env"


settings = Settings() # type: ignore[call-arg]