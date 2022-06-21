#reading module for GTFS files
import sys
from pathlib import Path

import gtfs_kit as gk

import pandas as pd
import numpy as np

import os

DIR = Path('..')
sys.path.append(str(DIR))

DATA_DIR = DIR/'DATA/'

def rectangles(feed) :
    rect = []
    df = feed.stop_times.join(feed.trips.set_index('trip_id'), on='trip_id').join(feed.stops.set_index('stop_id'), on='stop_id')[['route_id', 'stop_lon', 'stop_lat']]
    for route_id in df['route_id'].drop_duplicates() :
        lat = [x for x in df[df['route_id'] == route_id]["stop_lat"]]
        lon = [x for x in df[df['route_id'] == route_id]["stop_lon"]]
        rect.append([max(lat), max(lon), min(lat), min(lon), route_id])
    return pd.DataFrame(rect, columns=['lat_max', 'lon_max', 'lat_min', 'lon_min', 'route_id'])

rect = pd.DataFrame(np.array([[0.,0.,0.,0.,0.]]), columns = ["lat_max", "lon_max", "lat_min", "lon_min", "route_id"])

for name in os.listdir(DATA_DIR) :
    try :
        path = DATA_DIR/name
        feed = gk.read_feed(path, dist_units='km')
        rect = pd.concat([rect, rectangles(feed)])
    except :
        pass

rect.index = range(1900)

rect[1:].to_csv(path_or_buf="rectangles.csv")

