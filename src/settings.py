from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
import requests

token_endpoint = "https://www.strava.com/oauth/token"


class Settings(BaseSettings):
    client_id: str = Field()
    client_secret: str = Field()
    refresh_token: str = Field()
    access_token: str = None

    @field_validator("access_token", mode="before")
    def get_acces_token(cls, v, values, **kwargs):
        payload: dict = {
            "client_id": values.data["client_id"],
            "client_secret": values.data["client_secret"],
            "refresh_token": values.data["refresh_token"],
            "grant_type": "refresh_token",
            "f": "json",
        }
        res = requests.post(token_endpoint, data=payload, verify=False)
        access_token = res.json()["access_token"]
        return access_token


def get_settings() -> Settings:
    return Settings()
