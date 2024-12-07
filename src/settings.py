from pydantic import Field
from pydantic_settings import BaseSettings
import requests

token_endpoint = "https://www.strava.com/oauth/token"


class Settings(BaseSettings):
    client_id: str = Field()
    client_secret: str = Field()
    website_url: str = Field()
    access_token: str = ""

    @property
    def authorize_url(self) -> str:
        return (
            f"http://www.strava.com/oauth/authorize"
            f"?client_id={self.client_id}&response_type=code"
            f"&redirect_uri={self.website_url}/&approval_prompt=force&scope=activity:read_all"
        )

    def retrieve_access_token(self, auth_code: str):
        payload: dict = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "f": "json",
        }
        with requests.Session() as session:
            session.verify = True
            res = session.post(token_endpoint, data=payload)
            res.raise_for_status()
            access_token = res.json()["access_token"]

def get_settings() -> Settings:
    return Settings()


def get_Client_ID():
    return Settings().client_id

