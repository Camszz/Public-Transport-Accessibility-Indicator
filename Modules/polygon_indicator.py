import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def polygon_to_array(df_polygon, n_points=500) :
    lat_min, lat_max, lon_min, lon_max = df_polygon['latitude'].min(), df_polygon['latitude'].max(), df_polygon['longitude'].min(), df_polygon['longitude'].max()

    DeltaLAT, DeltaLON = lat_max-lat_min, lon_max-lon_min
    
    coords_lat = np.linspace(lat_max, lat_min, n_points)
    coords_lon = np.linspace(lon_min, lon_max, n_points)

    coords_array = np.matmul(coords_lat.T, coords_lon)
    return coords_array

data = gpd.read_file("https://france-geojson.gregoiredavid.fr/repo/departements/69-rhone/arrondissements-69-rhone.geojson")
print(data.head())