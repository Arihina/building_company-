from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    APP_SECRET_KEY: str

    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USE_TLS: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    @property
    def db_url(self):
        # postgresql://user:password@host:port/dbname
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def app_secret_key(self):
        return self.APP_SECRET_KEY

    @property
    def mail_server(self):
        return self.MAIL_SERVER

    @property
    def mail_port(self):
        return self.MAIL_PORT

    @property
    def mail_use_tls(self):
        return self.MAIL_USE_TLS

    @property
    def mail_username(self):
        return self.MAIL_USERNAME

    @property
    def mail_password(self):
        return self.MAIL_PASSWORD

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
