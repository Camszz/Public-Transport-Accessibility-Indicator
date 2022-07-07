import sys
from pathlib import Path
import os

import pandas as pd


def create_rectangles(feed):
    rect = []
    df = feed.stop_times.join(feed.trips.set_index("trip_id"), on="trip_id").join(
        feed.stops.set_index("stop_id"), on="stop_id"
    )[["route_id", "stop_lon", "stop_lat"]]
    agency_name = feed.agency['agency_name'].iloc[0]
    for route_id in df["route_id"].drop_duplicates():
        lat = [x for x in df[df["route_id"] == route_id]["stop_lat"]]
        lon = [x for x in df[df["route_id"] == route_id]["stop_lon"]]
        rect.append([max(lat), max(lon), min(lat), min(lon), route_id, agency_name])
    return pd.DataFrame(
        rect, columns=["lat_max", "lon_max", "lat_min", "lon_min", "route_id", "agency_name"]
    )
