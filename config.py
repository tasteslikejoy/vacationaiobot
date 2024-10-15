from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_token: SecretStr
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file='.env',
        env_file_ncoding='utf-8'
    )

config = Settings()


