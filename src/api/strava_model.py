from typing import List
from pydantic import BaseModel, Field


class ExplorerSegment(BaseModel):
    id: int = Field(description="The unique identifier of this segment")
    resource_state: int = Field(description="The resource state of this segment")
    name: str = Field(description="The name of this segment")
    climb_category: int = Field(
        description="The category of the climb [0, 5]. Higher is harder ie. 5 is Hors catégorie, 0 is uncategorized in climb_category. If climb_category = 5, climb_category_desc = HC. If climb_category = 2, climb_category_desc = 3."
    )
    climb_category_desc: str = Field(
        description="The description for the category of the climb May take one of the following values: NC, 4, 3, 2, 1, HC"
    )
    avg_grade: float = Field(description="The segment's average grade, in percents")
    start_latlng: List[float] = Field(description="An instance of LatLng.")
    end_latlng: List[float] = Field(description="An instance of LatLng.")
    elev_difference: float = Field(description="The segments's evelation difference, in meters")
    distance: float = Field(description="The segment's distance, in meters")
    points: str = Field(description="The polyline of the segment")
    starred: bool = Field(
        description="Whether this segment is starred by the authenticated athlete"
    )
    elevation_profile: str = Field(description="The URL for the segment's elevation profile image")
    local_legend_enabled: bool = Field(description="Whether the segment has local legend enabled")


class ExplorerResponse(BaseModel):
    segments: List[ExplorerSegment] = Field(description="The list of segments")


class AthleteSegmentStats(BaseModel):
    pr_elapsed_time: int | None = Field(description="The elapsed time ot the PR effort")
    pr_date: str | None = Field(description="The time at which the PR effort was started")
    pr_visibility: str | None = Field(
        description="Visibility of the PR effort. May take one of the following values: everyone, only_me"
    )
    pr_activity_id: int | None = Field(
        description="The unique identifier of the activity related to the PR effort"
    )
    pr_activity_visibility: str | None = Field(
        description="Visibility of the activity related to the PR effort. May take one of the following values: everyone, only_me"
    )
    effort_count: int | None = Field(
        description="Number of efforts by the authenticated athlete on this segment"
    )


class PolylineMap(BaseModel):
    id: str = Field(description="The identifier of the map")
    polyline: str = Field(
        description="The polyline of the map, only returned on detailed representation of an object"
    )
    resource_state: int = Field(description="The resource state of the map")


class EffortCounts(BaseModel):
    overall: str | None = Field(description="The overall best effort count as a string")
    female: str | None = Field(description="The best effort count for the female")


class LocalLegendAthlete(BaseModel):
    athlete_id: int = Field(description="The unique identifier of the athlete")
    title: str = Field(description="The name of the athlete")
    profile: str = Field(description="The URL of the athlete's profile picture")
    effort_description: str = Field(
        description="Number of times the athlete has completed the segment as a text"
    )
    effort_count: int = Field(description="Number of times the athlete has completed the segment")
    effort_counts: EffortCounts = Field(description="Dunnno what this is")
    destination: str = Field(description="")


class XomDestination(BaseModel):
    href: str = Field(description="The URL for the destination")
    type: str = Field(description="The type of the destination")
    name: str = Field(description="The name of the destination")


class Xoms(BaseModel):
    kom: str = Field(description="The time at which the KOM was achieved")
    qom: str = Field(description="The time at which the QOM was achieved")
    overall: str = Field(description="The time at which the overall best time was achieved")
    destination: XomDestination = Field(description="Dunno what this is")


class DetailedSegment(BaseModel):
    id: int = Field(description="The unique identifier of this segment")
    resource_state: int = Field(description="The resource state of this segment")
    name: str = Field(description="The name of this segment")
    activity_type: str = Field(description="May take one of the following values: Ride, Run")
    distance: float = Field(description="The segment's distance, in meters")
    average_grade: float = Field(description="The segment's average grade, in percents")
    maximum_grade: float = Field(description="The segments's maximum grade, in percents")
    elevation_high: float = Field(description="The segments's highest elevation, in meters")
    elevation_low: float = Field(description="The segments's lowest elevation, in meters")
    start_latlng: List[float] = Field(description="An instance of LatLng.")
    end_latlng: List[float] = Field(description="An instance of LatLng.")
    elevation_profile: str = Field(description="The URL for the segment's elevation profile image")
    climb_category: int = Field(
        description="The category of the climb [0, 5]. Higher is harder ie. 5 is Hors catégorie, 0 is uncategorized in climb_category."
    )
    city: str | None = Field(description="The segments's city.")
    state: str | None = Field(description="The segments's state or geographical region.")
    country: str | None = Field(description="The segment's country.")
    private: bool = Field(description="Whether this segment is private.")
    hazardous: bool = Field(description="Whether this segment is considered hazardous.")
    starred: bool = Field(
        description="Whether this segment is starred by the authenticated athlete."
    )
    created_at: str = Field(description="The time at which the segment was created.")
    updated_at: str = Field(description="The time at which the segment was last updated.")
    total_elevation_gain: float = Field(description="The segment's total elevation gain.")
    map: PolylineMap = Field(description="An instance of PolylineMap.")
    effort_count: int = Field(description="The total number of efforts for this segment")
    athlete_count: int = Field(
        description="The number of unique athletes who have an effort for this segment"
    )
    star_count: int = Field(description="The number of stars for this segment")
    athlete_segment_stats: AthleteSegmentStats = Field(
        description="An instance of AthleteSegmentStats."
    )
    xoms: Xoms = Field(description="An instance of Xoms.")
    local_legend: LocalLegendAthlete = Field(description="An instance of LocalLegendAthlete.")
