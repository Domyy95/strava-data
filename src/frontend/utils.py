from math import pi, cos
from datetime import datetime, timedelta
import json
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go


def create_square(lat, lon, square_size=1600):
    R = 6378000.0  # Earth radius in meters

    # Coordinate offsets in radians
    d_lat = (square_size / 2) / R
    d_lon = (square_size / 2) / (R * cos(pi * lat / 180))

    d_lat = d_lat * (180 / pi)
    d_lon = d_lon * (180 / pi)

    sw = [lat - d_lat, lon - d_lon]  # Southwest
    nw = [lat + d_lat, lon - d_lon]  # Northwest
    ne = [lat + d_lat, lon + d_lon]  # Northeast
    se = [lat - d_lat, lon + d_lon]  # Southeast

    return [sw, nw, ne, se, sw]


def convert_seconds_to_hm(seconds):
    negative = False
    if seconds < 0:
        negative = True
        seconds = abs(seconds)

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)

    if hours > 0:
        result = f"{hours}:{minutes:02d}:{remaining_seconds:02d}"
    else:
        result = f"{minutes}:{remaining_seconds:02d}"

    if negative:
        result = "-" + result

    return result


def get_data_run(block, span):
    with open("runs.json") as json_run:
        runs = json.load(json_run)
        return iterate_over_runs(runs, span, block)


def iterate_over_runs(runs, span, block):
    runs_dict = {}

    for n in range(span):
        runs_dict[n] = [0, 0, 0]

    for page in runs:
        for run in page:
            if run["sport_type"] == "Run" or run["sport_type"] == "TrailRun":
                run_date = run["start_date"].split("T")[0]
                span_delta = time_beetween(run_date, block)
                if span_delta < span:
                    km, time_duration, elevation = runs_dict[span_delta]
                    runs_dict[span_delta] = [
                        km + run["distance"],
                        time_duration + run["elapsed_time"],
                        elevation + run["total_elevation_gain"],
                    ]

    distance, times, gain = [], [], []

    for m, t, d in runs_dict.values():
        distance.append(m / 1000)
        times.append(t / 3600)
        gain.append(d)

    x = build_x_axis(block, span)

    return x[::-1], distance[::-1], gain[::-1], times[::-1]


def build_x_axis(block, span):
    current_date = datetime.now()
    ranges = []
    for _ in range(span):
        if block == "Months":
            # Start and end of the current month
            range_start = current_date.replace(day=1)
            range_end = (range_start + relativedelta(months=1)) - relativedelta(days=1)
            current_date = range_start - relativedelta(months=1)  # Move to the previous month
        elif block == "Weeks":
            range_start = current_date - timedelta(days=current_date.weekday())  # Monday
            range_end = range_start + timedelta(days=6)  # Sunday
            current_date = range_start - timedelta(days=7)  # Move to the previous week
        elif block == "Years":
            # Start and end of the current year
            range_start = current_date.replace(month=1, day=1)
            range_end = current_date.replace(month=12, day=31)
            current_date = range_start - relativedelta(years=1)  # Move to the previous year

        ranges.append(range_start.strftime("%Y-%m-%d") + " - " + range_end.strftime("%Y-%m-%d"))

    return ranges


def time_beetween(run_date, block):
    current_date = datetime.now()
    run_date = datetime.strptime(run_date, "%Y-%m-%d")
    if block == "Weeks":
        current_start_of_week = current_date - timedelta(days=current_date.weekday())
        run_start_of_week = run_date - timedelta(days=run_date.weekday())
        # Calculate the difference in days and divide by 7
        difference = (current_start_of_week - run_start_of_week).days
        return abs(difference // 7)
    elif block == "Months":
        # Use relativedelta to calculate months
        delta = relativedelta(current_date, run_date)
        return abs(delta.years * 12 + delta.months)
    elif block == "Years":
        # Use relativedelta to calculate years
        delta = relativedelta(current_date, run_date)
        return abs(delta.years)


def make_charts_figure(x, km, gain, mins, chart, color):
    if chart != "bar":
        fig_distance = go.Figure()
        fig_hr = go.Figure()
        fig_gain = go.Figure()

        fig_distance.add_trace(go.Scatter(x=x, y=km, marker_color=color))
        fig_gain.add_trace(go.Scatter(x=x, y=gain, marker_color=color))
        fig_hr.add_trace(go.Scatter(x=x, y=mins, marker_color=color))

        return fig_distance, fig_gain, fig_hr
    else:
        fig_distance = go.Figure()
        fig_hr = go.Figure()
        fig_gain = go.Figure()

        fig_distance.add_trace(go.Bar(x=x, y=km, marker_color=color))
        fig_gain.add_trace(go.Bar(x=x, y=gain, marker_color=color))
        fig_hr.add_trace(go.Bar(x=x, y=mins, marker_color=color))

        return fig_distance, fig_gain, fig_hr
