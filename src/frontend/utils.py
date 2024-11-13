from math import pi, cos
from datetime import datetime, timedelta
import json


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


def get_data_run(time_week_x, code):
    runs_dict = {}
    first_day = time_week_x[0].split(" ")[0].replace("/", "-")

    for number_week_counter in range(len(time_week_x)):
        runs_dict[number_week_counter] = [0, 0, 0]

    with open(f"runs{code}.json") as json_run:
        runs = json.load(json_run)

        for page in runs:
            for run in page:
                if run["sport_type"] == "Run" or run["sport_type"] == "TrailRun":
                    run_date = run["start_date"].split("T")[0]
                    weeks_delta = weeks_between(first_day, run_date)
                    if weeks_delta >= 0:
                        km, time_duration, elevation = runs_dict[weeks_delta]
                        runs_dict[weeks_delta] = [
                            km + run["distance"],
                            time_duration + run["elapsed_time"],
                            elevation + run["total_elevation_gain"],
                        ]

    distance, times, gain = [], [], []

    for m, t, d in runs_dict.values():
        distance.append(m / 1000)
        times.append(t / 3600)
        gain.append(d)

    return runs_dict, distance, times, gain


def get_weeks(years):
    # Parse i dati di input

    current_datetime = datetime.now().strftime("%Y-%m-%d")
    input_date = datetime.strptime(current_datetime, "%Y-%m-%d")

    # Ottieni l'anno corrente e i tre anni precedenti
    current_year = input_date.year
    target_years = [current_year - i for i in range(years, 0, -1)] + [current_year]
    # Lista per contenere le informazioni su tutte le settimane
    all_weeks_info = []

    # Cicla su ciascun anno nei target_years
    for target_year in target_years:
        # Trova il primo lunedì dell'anno
        first_day_of_year = datetime(target_year, 1, 1)
        first_monday = first_day_of_year + timedelta(days=(7 - first_day_of_year.weekday()) % 7)

        # Scorri attraverso ogni settimana dell'anno
        current_monday = first_monday
        week_number = 1

        while current_monday.year == target_year:
            # Calcola la domenica di quella settimana
            current_sunday = current_monday + timedelta(days=6)

            # Se siamo nell'anno corrente e superiamo la data fissata, interrompi il ciclo
            if target_year == current_year and current_monday > input_date:
                break

            # Aggiungi le informazioni della settimana alla lista
            all_weeks_info.append(
                {
                    "year": target_year,
                    "week_number": week_number,
                    "monday_start": current_monday.date(),
                    "sunday_finish": current_sunday.date(),
                }
            )

            # Passa al lunedì successivo
            current_monday += timedelta(weeks=1)
            week_number += 1

    # Ordina le settimane in ordine cronologico basato sulla data di inizio
    all_weeks_info.sort(key=lambda week: week["monday_start"])

    date_time_x = []
    date_time = []

    # Stampa i risultati
    for week in all_weeks_info:
        date_time_x.append(
            f"{week['year']}-{week['monday_start'].month}/{week['monday_start'].day} to {week['sunday_finish'].month}/{week['sunday_finish'].day}"
        )
        date_time.append([week["year"], [week["monday_start"], week["sunday_finish"]]])

    return date_time, date_time_x


def weeks_between(start_date_str, end_date_str):
    # Converti le stringhe di data in oggetti datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Calcola la differenza tra le due date in giorni
    days_difference = (end_date - start_date).days

    # Converti la differenza in settimane
    weeks_difference = days_difference // 7  # Divisione intera per ottenere settimane complete

    return weeks_difference
