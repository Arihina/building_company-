from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    APP_SECRET_KEY: str

    @property
    def db_url(self):
        # postgresql://user:password@host:port/dbname
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def app_secret_key(self):
        return self.APP_SECRET_KEY

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
