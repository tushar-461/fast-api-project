import os


class Settings:
    def __init__(self) -> None:
        self.secret_key = os.getenv("SECRET_KEY", "secret123")
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()


settings = Settings()
