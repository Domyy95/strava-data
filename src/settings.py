from pydantic import Field
from pydantic_settings import BaseSettings
import requests

token_endpoint = "https://www.strava.com/oauth/token"


class Settings(BaseSettings):
    client_id: str = Field()
    client_secret: str = Field()
    website_url: str = Field()
    auth_code: str = ""
    access_token: str = ""

    def get_access_token(self, auth_code):
        self.auth_code = auth_code
        self.retrieve_access_token()

    def retrieve_access_token(self):
        payload: dict = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.auth_code,
            "grant_type": "authorization_code",
            "f": "json",
        }
        with requests.Session() as session:
            session.verify = True
            res = session.post(token_endpoint, data=payload)
            res.raise_for_status()
            access_token = res.json()["access_token"]

        self.access_token = access_token
