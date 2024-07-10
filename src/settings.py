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
    def get_access_token(cls, v, values, **kwargs):
        print("Getting access token")
        payload: dict = {
            "client_id": values.data["client_id"],
            "client_secret": values.data["client_secret"],
            "refresh_token": values.data["refresh_token"],
            "grant_type": "refresh_token",
            "f": "json",
        }
        with requests.Session() as session:
            session.verify = True
            res = session.post(token_endpoint, data=payload)
            res.raise_for_status()
            access_token = res.json()["access_token"]
            return access_token


def get_settings() -> Settings:
    return Settings()
