from typing import List
import requests

from src.api.strava_model import DetailedSegment, ExplorerResponse, ExplorerSegment

BASE_URL = "https://www.strava.com/api/v3/"


class StravaAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.get_url = BASE_URL + "{endpoint}" + "?access_token=" + self.access_token

    def explore_segments(
        self,
        bottom_left_point: List[float],
        top_right_point: List[float],
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

    def get_segment(self, segment_id: int) -> DetailedSegment:
        """
        Returns the specified segment data.
        segment_id: The identifier of the segment.
        """
        url = self.get_url.format(endpoint=f"segments/{segment_id}")
        api_response = requests.get(url)
        return DetailedSegment.model_validate(api_response.json())
