from typing import List, Optional
from pydantic import BaseModel, Field
from src.api.strava_enums import SportType, ActivityType


class SummaryGear(BaseModel):
    id: str = Field(description="The gear's unique identifier")
    primary: bool = Field(description="Whether this gear's is the owner's default one")
    name: str = Field(description="The gear's name")
    nickname: str = Field(description="The gear's nickname")
    resource_state: int = Field(
        description="Resource state, indicates level of detail. Possible values: 2 -> summary, 3 -> detail"
    )
    retired: bool = Field(description="Whether this gear is retired")
    distance: float = Field(description="The distance logged with this gear")
    converted_distance: float = Field(description="The distance logged with this gear")


class SummaryClub(BaseModel):
    id: int = Field(description="The club's unique identifier")
    resource_state: int = Field(
        description="Resource state, indicates level of detail. Possible values: 1 -> meta, 2 -> summary, 3 -> detail"
    )
    name: str = Field(description="The club's name")
    profile_medium: str = Field(description="URL to a 60x60 pixel profile picture")
    cover_photo: str = Field(description="URL to a ~1185x580 pixel cover photo")
    cover_photo_small: str = Field(description="URL to a ~360x176 pixel cover photo")
    activity_types: List[ActivityType] = Field(
        description="The activity types that count for a club. This takes precedence over sport_type."
    )
    activity_types_icon: str = Field(description="icon name of the club's activity types")
    dimensions: List[str] = Field(description="The club's stats dimensions")
    sport_type: str = Field(
        description="Deprecated. Prefer to use activity_types. May take one of the following values: cycling, running, triathlon, other"
    )
    localized_sport_type: str = Field(description="The club's localized sport type")
    city: str = Field(description="The club's city")
    state: str = Field(description="The club's state or geographical region")
    country: str = Field(description="The club's country")
    private: bool = Field(description="Whether the club is private")
    member_count: int = Field(description="The club's member count")
    featured: bool = Field(description="Whether the club is featured or not")
    verified: bool = Field(description="Whether the club is verified or not")
    url: str = Field(description="The club's vanity URL")
    membership: str = Field(
        description="The authenticated athlete's membership status of the club."
    )
    admin: bool = Field(description="Whether the authenticated athlete is an admin of the club")
    owner: bool = Field(description="Whether the authenticated athlete is the owner of the club")


class DetailedAthlete(BaseModel):
    id: int = Field(description="The unique identifier of the athlete")
    username: str = Field(description="The athlete's username")
    resource_state: int = Field(description="The resource state of the athlete")
    firstname: str = Field(description="The athlete's first name")
    lastname: str = Field(description="The athlete's last name")
    bio: str = Field(description="The athlete's profile bio")
    city: str = Field(description="The athlete's city")
    state: Optional[str] = Field(description="The athlete's state")
    country: Optional[str] = Field(description="The athlete's country")
    sex: str = Field(description="The athlete's sex. May take one of the following values: M, F")
    premium: bool = Field(
        description="Deprecated. Use summit field instead. Whether the athlete has any Summit subscription."
    )
    summit: bool = Field(description="Whether the athlete has any Summit subscription")
    created_at: str = Field(description="The time at which the athlete was created")
    updated_at: str = Field(description="The time at which the athlete was last updated")
    badge_type_id: int = Field(description="The badge type id of the athlete")
    weight: float = Field(description="The athlete's weight")
    profile_medium: str = Field(description="URL to a 62x62 pixel profile picture")
    profile: str = Field(description="URL to a 124x124 pixel profile picture")
    friend: Optional[str] = Field(description="The athlete's friend status")
    follower: Optional[str] = Field(description="The athlete's follower status")
    blocked: bool = Field(description="The athlete's blocked status")
    can_follow: bool = Field(description="The athlete's follow status")
    follower_count: int = Field(description="The athlete's follower count")
    friend_count: int = Field(description="The athlete's friend count")
    mutual_friend_count: int = Field(description="The athlete's mutual friend count")
    athlete_type: int = Field(description="The athlete's type")
    date_preference: str = Field(description="The athlete's date preference. Format '%m/%d/%Y")
    measurement_preference: str = Field(
        description="The athlete's preferred unit system. May take one of the following values: feet, meters"
    )
    clubs: List[SummaryClub] = Field(description="The athlete's clubs")
    postable_clubs_count: int = Field(description="The number of clubs the athlete can post to")
    ftp: Optional[int] = Field(description="The athlete's FTP (Functional Threshold Power)")
    bikes: List[SummaryGear] = Field(description="The athlete's bikes")
    shoes: List[SummaryGear] = Field(description="The athlete's shoes")
    is_winback_via_upload: bool = Field(description="Whether the athlete is a winback via upload")
    is_winback_via_view: bool = Field(description="Whether the athlete is a winback via view")


class ActivityTotal(BaseModel):
    count: int = Field(description="The total number of activities.")
    distance: float = Field(description="The total distance covered.")
    moving_time: int = Field(description="The total moving time.")
    elapsed_time: int = Field(description="The total elapsed time.")
    elevation_gain: float = Field(description="The total elevation gain.")
    achievement_count: Optional[int] = Field(
        default=None, description="The total number of achievements."
    )


class ActivityStats(BaseModel):
    biggest_ride_distance: float = Field(description="The longest distance ridden by the athlete.")
    biggest_climb_elevation_gain: float = Field(
        description="The highest elevation climbed by the athlete."
    )
    recent_ride_totals: ActivityTotal = Field(description="Last month ride totals.")
    all_ride_totals: ActivityTotal = Field(description="The all time ride totals.")
    recent_run_totals: ActivityTotal = Field(description="Last month run totals.")
    all_run_totals: ActivityTotal = Field(description="The all time run totals.")
    recent_swim_totals: ActivityTotal = Field(description="Last month swim totals.")
    all_swim_totals: ActivityTotal = Field(description="The all time swim totals.")
    ytd_ride_totals: ActivityTotal = Field(description="The year to date ride totals.")
    ytd_run_totals: ActivityTotal = Field(description="The year to date run totals.")
    ytd_swim_totals: ActivityTotal = Field(description="The year to date swim totals.")


# Explore segment and segment objects
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
    pr_elapsed_time: Optional[int] = Field(description="The elapsed time ot the PR effort")
    pr_date: Optional[str] = Field(description="The time at which the PR effort was started")
    pr_visibility: Optional[str] = Field(
        description="Visibility of the PR effort. May take one of the following values: everyone, only_me"
    )
    pr_activity_id: Optional[int] = Field(
        description="The unique identifier of the activity related to the PR effort"
    )
    pr_activity_visibility: Optional[str] = Field(
        description="Visibility of the activity related to the PR effort. May take one of the following values: everyone, only_me"
    )
    effort_count: Optional[int] = Field(
        description="Number of efforts by the authenticated athlete on this segment"
    )


class PolylineMap(BaseModel):
    id: str = Field(description="The identifier of the map")
    polyline: str = Field(
        description="The polyline of the map, only returned on detailed representation of an object"
    )
    resource_state: int = Field(description="The resource state of the map")


class EffortCounts(BaseModel):
    overall: Optional[str] = Field(description="The overall best effort count as a string")
    female: Optional[str] = Field(description="The best effort count for the female")


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
    qom: Optional[str] = Field(description="The time at which the QOM was achieved")
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
    city: Optional[str] = Field(description="The segments's city.")
    state: Optional[str] = Field(description="The segments's state or geographical region.")
    country: Optional[str] = Field(description="The segment's country.")
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
    local_legend: Optional[LocalLegendAthlete] = Field(
        description="An instance of LocalLegendAthlete."
    )


# Get Activity and Activity Laps Objects
class MetaAthlete(BaseModel):
    id: int = Field(description="The unique identifier of the athlete")
    resource_state: int = Field(description="The resource state of the athlete")


class MetaActivity(BaseModel):
    id: int = Field(description="The unique identifier of the activity")
    visibility: str = Field(
        description="The visibility of the activity. May take one of the following values: everyone, only_me"
    )
    resource_state: int = Field(description="The resource state of the activity")


class Lap(BaseModel):
    id: int = Field(description="The unique identifier of this lap")
    resource_state: int = Field(description="The resource state of the lap")
    name: str = Field(description="The name of the lap")
    activity: MetaActivity = Field(description="Unique identifier of the activity")
    athlete: MetaAthlete = Field(description="Unique identifier of the athlete")
    elapsed_time: int = Field(description="The lap's elapsed time, in seconds")
    moving_time: int = Field(description="The lap's moving time, in seconds")
    start_date: str = Field(description="The time at which the lap was started.")
    start_date_local: str = Field(
        description="The time at which the lap was started in the local timezone."
    )
    distance: float = Field(description="The lap's distance, in meters")
    average_speed: float = Field(description="The lap's average speed")
    max_speed: float = Field(description="The maximum speed of this lat, in meters per second")
    lap_index: int = Field(description="The index of this lap in the activity it belongs to")
    split: int = Field(description="An instance of integer.")
    start_index: int = Field(description="The start index of this effort in its activity's stream")
    end_index: int = Field(description="The end index of this effort in its activity's stream")
    total_elevation_gain: float = Field(description="The elevation gain of this lap, in meters")
    average_cadence: float = Field(description="The lap's average cadence")
    device_watts: bool = Field(
        description="For riding efforts, whether the wattage was reported by a dedicated recording device"
    )
    average_watts: float = Field(description="The average wattage of this lap")
    pace_zone: int = Field(description="The athlete's pace zone during this lap")
    average_heartrate: Optional[float] = Field(
        description="The average heart rate of this lap.", default=None
    )
    max_heartrate: Optional[float] = Field(
        description="The maximum heart rate of this lap", default=None
    )


class Laps(BaseModel):
    laps: List[Lap] = Field(description="A collection of Lap objects.")


class PhotosSummary_primary(BaseModel):
    id: int = Field(description="The unique identifier of the photo")
    source: int = Field(description="The source of the photo")
    unique_id: str = Field(description="The unique identifier of the photo")
    urls: str = Field(description="The URL of the photo")


class PhotosSummary(BaseModel):
    primary: Optional[PhotosSummary_primary] = Field(description="The URL of the primary photo")
    count: int = Field(description="The number of photos")


class SummarySegment(BaseModel):
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
    elevation_profile: Optional[str] = Field(
        description="The URL for the segment's elevation profile image"
    )
    elevation_profiles: Optional[str] = Field(
        description="The URL for the segment's elevation profile image"
    )
    climb_category: int = Field(
        description="The category of the climb [0, 5]. Higher is harder ie. 5 is Hors catégorie, 0 is uncategorized in climb_category."
    )
    city: Optional[str] = Field(description="The segments's city.")
    state: Optional[str] = Field(description="The segments's state or geographical region.")
    country: Optional[str] = Field(description="The segment's country.")
    private: bool = Field(description="Whether this segment is private.")
    hazardous: bool = Field(description="Whether this segment is considered hazardous.")
    starred: bool = Field(
        description="Whether this segment is starred by the authenticated athlete."
    )


class SegmentEffort(BaseModel):
    id: int = Field(description="The unique identifier of this effort")
    resource_state: int = Field(description="The resource state of this effort")
    name: str = Field(description="The name of the segment on which this effort was performed")
    activity: MetaActivity = Field(description="An instance of MetaActivity.")
    athlete: MetaAthlete = Field(description="An instance of MetaAthlete.")
    elapsed_time: int = Field(description="The effort's elapsed time")
    moving_time: int = Field(description="The effort's moving time")
    start_date: str = Field(description="The time at which the effort was started.")
    start_date_local: str = Field(
        description="The time at which the effort was started in the local timezone."
    )
    distance: float = Field(description="The effort's distance in meters")
    achievements: List[str] = Field(description="The achievements of the effort")
    start_index: int = Field(description="The start index of this effort in its activity's stream")
    end_index: int = Field(description="The end index of this effort in its activity's stream")


class DetailedSegmentEffort(SegmentEffort):
    average_cadence: float = Field(description="The effort's average cadence")
    device_watts: bool = Field(
        description="For riding efforts, whether the wattage was reported by a dedicated recording device"
    )
    average_watts: float = Field(description="The average wattage of this effort")
    average_heartrate: float = Field(
        description="The heart heart rate of the athlete during this effort"
    )
    max_heartrate: float = Field(
        description="The maximum heart rate of the athlete during this effort"
    )
    segment: SummarySegment = Field(description="An instance of SummarySegment.")
    pr_rank: Optional[int] = Field(
        description="The rank of the effort on the athlete's leaderboard if it belongs in the top 3 at the time of upload"
    )
    visibility: str = Field(
        description="The visibility of the effort. May take one of the following values: everyone, only_me"
    )
    kom_rank: Optional[int] = Field(
        description="The rank of the effort on the global leaderboard if it belongs in the top 10 at the time of upload"
    )
    hidden: bool = Field(
        description="Whether this effort should be hidden when viewed within an activity"
    )


class StatVisibility(BaseModel):
    type: str = Field(description="Type of parameter")
    visibility: str = Field(
        description="Visibility of the parameter. May take one of the following values: everyone, only_me"
    )


class Trend(BaseModel):
    speeds: List[float] = Field(description="The speed of the activity")
    current_activity_index: int = Field(description="The index of the current activity")
    min_speed: float = Field(description="The minimum speed of the activity")
    mid_speed: float = Field(description="The mid speed of the activity")
    max_speed: float = Field(description="The maximum speed of the activity")
    direction: int = Field(description="The direction of the activity")


class SimilarActivity(BaseModel):
    effort_count: int = Field(description="Effort perceved")
    average_speed: float = Field(description="The average speed of the activity")
    min_average_speed: float = Field(description="The minimum average speed of the activity")
    mid_average_speed: float = Field(description="The mid average speed of the activity")
    max_average_speed: float = Field(description="The maximum average speed of the activity")
    pr_rank: Optional[int] = Field(
        description="The rank of the effort on the athlete's leaderboard if it belongs in the top 3 at the time of upload"
    )
    frequency_milestone: Optional[int] = Field(description="The frequency of the milestone")
    trend: Trend = Field(description="The trend of the activity")
    resource_state: int = Field(description="The resource state of the activity")


class SplitMetric(BaseModel):
    distance: float = Field(description="The distance of the split")
    elapsed_time: int = Field(description="The elapsed time of the split")
    elevation_difference: float = Field(description="The elevation difference of the split")
    moving_time: int = Field(description="The moving time of the split")
    split: int = Field(description="The split")
    average_speed: float = Field(description="The average speed of the split")
    average_grade_adjusted_speed: float = Field(
        description="The average grade adjusted speed of the split"
    )
    average_heartrate: float = Field(description="The average heart rate of the split")
    pace_zone: int = Field(description="The pace zone of the split")


class DetailedActivity(BaseModel):
    id: int = Field(description="The unique identifier of the activity")
    resource_state: int = Field(description="The resource state of the lap")
    external_id: str = Field(description="The identifier provided at upload time")
    upload_id: int = Field(
        description="The identifier of the upload that resulted in this activity"
    )
    athlete: MetaAthlete = Field(description="An instance of MetaAthlete.")
    name: str = Field(description="The name of the activity")
    distance: float = Field(description="The activity's distance, in meters")
    moving_time: int = Field(description="The activity's moving time, in seconds")
    elapsed_time: int = Field(description="The activity's elapsed time, in seconds")
    total_elevation_gain: float = Field(description="The activity's total elevation gain.")
    elev_high: float = Field(description="The activity's highest elevation, in meters")
    elev_low: float = Field(description="The activity's lowest elevation, in meters")
    type: str = Field(description="Deprecated. Prefer to use sport_type")
    sport_type: SportType = Field(description="An instance of SportType.")
    start_date: str = Field(description="The time at which the activity was started.")
    start_date_local: str = Field(
        description="The time at which the activity was started in the local timezone."
    )
    timezone: str = Field(description="The timezone of the activity")
    utc_offset: int = Field(description="The UTC offset of the activity, in seconds")
    location_city: Optional[str] = Field(description="The city where the activity was started")
    location_state: Optional[str] = Field(description="The state where the activity was started")
    location_country: Optional[str] = Field(
        description="The country where the activity was started"
    )
    start_latlng: List[float] = Field(description="An instance of LatLng.")
    end_latlng: List[float] = Field(description="An instance of LatLng.")
    achievement_count: int = Field(
        description="The number of achievements gained during this activity"
    )
    kudos_count: int = Field(description="The number of kudos given for this activity")
    comment_count: int = Field(description="The number of comments for this activity")
    athlete_count: int = Field(
        description="The number of athletes for taking part in a group activity"
    )
    photo_count: int = Field(description="The number of Instagram photos for this activity")
    total_photo_count: int = Field(
        description="The number of Instagram and Strava photos for this activity"
    )
    map: PolylineMap = Field(description="An instance of PolylineMap.")
    trainer: bool = Field(description="Whether this activity was recorded on a training machine")
    commute: bool = Field(description="Whether this activity is a commute")
    manual: bool = Field(description="Whether this activity was created manually")
    private: bool = Field(description="Whether this activity is private")
    visibility: str = Field(
        description="The visibility of the activity. May take one of the following values: everyone, only_me"
    )
    flagged: bool = Field(description="Whether this activity is flagged")
    workout_type: int = Field(description="The activity's workout type")
    upload_id_str: str = Field(description="The unique identifier of the upload in string format")
    average_speed: float = Field(description="The activity's average speed, in meters per second")
    max_speed: float = Field(description="The activity's max speed, in meters per second")
    has_kudoed: bool = Field(description="Whether the logged-in athlete has kudoed this activity")
    hide_from_home: bool = Field(description="Whether the activity is muted")
    has_heartrate: bool = Field(description="Whether the activity has heartrate data")
    average_heartrate: float = Field(description="The activity's average heart rate")
    max_heartrate: float = Field(description="The activity's maximum heart rate")
    heartrate_opt_out: bool = Field(
        description="Whether the user has opted out of heartrate analysis"
    )
    display_hide_heartrate_option: bool = Field(
        description="Whether this activity should be hidden from heartrate analysis sections"
    )
    from_accepted_tag: bool = Field(description="Whether the activity was recorded on a device")
    pr_count: int = Field(description="The number of PRs gained during this activity")
    suffer_score: float = Field(description="The activity's suffer score")
    perceived_exertion: Optional[int] = Field(description="The activity's perceived exertion")
    prefer_perceived_exertion: bool = Field(
        description="Whether the user prefers the perceived exertion"
    )
    gear_id: str = Field(description="The id of the gear for the activity")
    kilojoules: float = Field(description="The total work done in kilojoules during this activity.")
    average_cadence: float = Field(description="The average cadence during this activity.")
    average_watts: float = Field(description="Average power output in watts during this activity.")
    device_watts: bool = Field(
        description="Whether the watts are from a power meter, false if estimated"
    )
    max_watts: int = Field(description="Rides with power meter data only")
    weighted_average_watts: int = Field(
        description="Similar to Normalized Power. Rides with power meter data only"
    )
    description: str = Field(description="The description of the activity")
    photos: PhotosSummary = Field(description="The URL of the activity's photos")
    gear: SummaryGear = Field(description="An instance of Gear.")
    calories: float = Field(description="The number of kilocalories consumed during this activity")
    segment_efforts: List[DetailedSegmentEffort] = Field(
        description="A collection of DetailedSegmentEffort objects."
    )
    device_name: str = Field(description="The name of the device used to record the activity")
    embed_token: str = Field(description="The token used to embed a Strava activity")
    splits_metric: List[SplitMetric] = Field(
        description="The splits of this activity in metric units (for runs)"
    )
    splits_standard: List[SplitMetric] = Field(
        description="The splits of this activity in imperial units (for runs)"
    )
    laps: List[Lap] = Field(description="A collection of Lap objects.")
    best_efforts: List[SegmentEffort] = Field(
        description="A collection of DetailedSegmentEffort objects."
    )
    stats_visibility: List[StatVisibility] = Field(
        description="The visibility of the activity's stats. May take one of the following values: everyone, only_me"
    )
    similar_activities: SimilarActivity = Field(description="The similar activities")
    available_zones: List[str] = Field(description="The available columns table for this activity")
