from src.api.strava import StravaAPI
from src.settings import get_settings
from src.frontend.frontend import map_select


def run():
    settings = get_settings()
    strava_api = StravaAPI(settings.access_token)
    map_select()
    # segments = strava_api.explore_segments(
    #     bottom_left_point=[45.768661, 9.452020], top_right_point=[45.790124, 9.496888]
    # )

    # for segment in segments.segments:
    #     detailed_segment = strava_api.get_segment(segment.id)
    #     print(detailed_segment.name, detailed_segment.distance, detailed_segment.average_grade)


if __name__ == "__main__":
    run()
