from typing import List
from functools import lru_cache
import requests
import json

from src.api.strava_model import (
    ActivityStats,
    DetailedAthlete,
    DetailedSegment,
    ExplorerResponse,
    ExplorerSegment,
    DetailedActivity,
    Laps,
    Lap,
)

BASE_URL = "https://www.strava.com/api/v3/"


class StravaAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.get_url = BASE_URL + "{endpoint}" + "?access_token=" + self.access_token
        self.authenticated_athlete = self.__get_authenticated_athlete()
        self.authenticated_athlete_stats = self.get_athlete_stats(self.authenticated_athlete.id)
        self.get_activities()

    def handle_api_error(self, api_response, activity_id: int):
        """Handles API errors and raises ValueError if the activity is not found."""
        if api_response.status_code == 404 or "errors" in api_response.json():
            error_message = api_response.json().get("message", "Unknown error")
            if error_message == "Resource Not Found":
                print(f"Error: Activity {activity_id} not found.")
                raise ValueError(f"Activity {activity_id} not found.")

        # Raise exception for other HTTP errors
        api_response.raise_for_status()

    def __get_authenticated_athlete(self):
        url = self.get_url.format(endpoint="/athlete")
        api_response = requests.get(url)
        return DetailedAthlete.model_validate(api_response.json())

    @lru_cache()
    def explore_segments(
        self,
        bottom_left_point: tuple[float],
        top_right_point: tuple[float],
        activity_type: str = "running",
        min_cat: int = None,
        max_cat: int = None,
    ) -> List[ExplorerSegment]:
        """
        Returns the top 10 segments matching a specified query.
        bottom_left_point: The latitude and longitude for the bottom left corner of the search area.
        top_right_point: The latitude and longitude for the top right corner of the search area.
        activity_type: Desired activity type. May take one of the following values: running, riding
        min_cat: The minimum climbing category.
        max_cat: The maximum climbing category.
        """
        url = self.get_url.format(endpoint="segments/explore")
        # southwest corner latitutde, southwest corner longitude, northeast corner latitude, northeast corner longitude
        bounds_str = ",".join(map(str, bottom_left_point + top_right_point))
        api_response = requests.get(
            url,
            params={
                "bounds": bounds_str,
                "activity_type": activity_type,
                "min_cat": min_cat,
                "max_cat": max_cat,
            },
        )

        explorer_response = ExplorerResponse.model_validate(api_response.json())
        return explorer_response.segments

    @lru_cache()
    def get_segment(self, segment_id: int) -> DetailedSegment:
        """
        Returns the specified segment data.
        segment_id: The identifier of the segment.
        """
        url = self.get_url.format(endpoint=f"segments/{segment_id}")
        api_response = requests.get(url)
        return DetailedSegment.model_validate(api_response.json())

    @lru_cache()
    def get_activity(self, activity_id: int) -> DetailedActivity:
        """
        Returns the specified activity data.
        activity_id: The identifier of the activity. https://www.strava.com/activities/{activity_id}
        """
        url = self.get_url.format(endpoint=f"activities/{activity_id}")

        try:
            api_response = requests.get(url)
            self.handle_api_error(api_response, activity_id)

        except ValueError:
            return None

        return DetailedActivity.model_validate(api_response.json())

    @lru_cache()
    def get_activity_laps(self, activity_id: int) -> List[Lap]:
        """
        Returns the laps of the specified activity.
        activity_id: The identifier of the activity. https://www.strava.com/activities/{activity_id}
        """
        url = self.get_url.format(endpoint=f"activities/{activity_id}/laps")
        api_response = requests.get(url)
        self.handle_api_error(api_response, activity_id)
        laps = Laps(laps=api_response.json())
        return laps.laps

    @lru_cache()
    def get_athlete_stats(self, profile_id: int):
        url = self.get_url.format(endpoint=f"/athletes/{profile_id}/stats")
        api_response = requests.get(url)
        return ActivityStats.model_validate(api_response.json())

    @lru_cache()
    def get_activities(self, max_pages: int = 10, per_page: int = 200):
        url = f"https://www.strava.com/api/v3/athlete/activities?access_token={self.access_token}&per_page={per_page}&page="

        data_dumps = []
        page = 1
        while True:
            response = requests.get(url + str(page))
            if not response.json() or page > max_pages:
                break

            page += 1
            data_dumps.append(response.json())

        with open("runs.json", "w") as outfile:
            json.dump(data_dumps, outfile, indent=4)
