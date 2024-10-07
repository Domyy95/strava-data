from math import pi, cos


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
