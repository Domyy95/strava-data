from src.api.strava import StravaAPI
from src.settings import get_settings
from src.frontend.home import home


def run():
    settings = get_settings()
    strava_api = StravaAPI(settings.access_token)
    home(strava_api)


if __name__ == "__main__":
    run()
