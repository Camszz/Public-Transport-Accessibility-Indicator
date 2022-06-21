import sys
from pathlib import Path
import os

import gtfs_kit as gk
import pandas as pd

import freq
import rectangles as rec

DIR = Path().resolve()

sys.path.append(str(DIR))

DATA_DIR = DIR/'DATA/'

df_rect = pd.DataFrame(columns = ["lat_max", "lon_max", "lat_min", "lon_min", "route_id"])

for name in os.listdir(DATA_DIR) :
    try :
        path = DATA_DIR/name
        feed = gk.read_feed(path, dist_units='km')
        df_rect = pd.concat([df_rect, rec.create_rectangles(feed)])
    except :
        pass

df_rect.to_csv(path_or_buf = "rectangles.csv", index=False)

df_freq = pd.DataFrame(columns = ["stop_id", "route_id", "bus_per_hour", "stop_lat", "stop_lon"])

for name in os.listdir(DATA_DIR) :
    try :
        path = DATA_DIR/name
        feed = gk.read_feed(path, dist_units='km')
        df_trips = feed.trips
        df_stimes = feed.stop_times
        df_cal = feed.calendar
        df_stops = feed.stops
        df_freq = pd.concat([df_freq, freq.freq(df_trips, df_stimes, df_stops, df_cal)])
    except :
        pass

df_freq.to_csv(path_or_buf = "freq.csv", index=False)