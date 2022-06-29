import pandas as pd
import numpy as np

marche_max = 1500


def distance(lat_a, lon_a, lat_b, lon_b):
    return (
        6371
        * 1e3
        * np.arccos(
            np.sin(np.radians(lat_a)) * np.sin(np.radians(lat_b))
            + np.cos(np.radians(lat_a))
            * np.cos(np.radians(lat_b))
            * np.cos(np.radians(lon_b) - np.radians(lon_a))
        )
    )


def rect_retenus(df_rect, lat, lon, rayon):
    """Selects the rectangle candidates that are close enough to potentially have a stop close to the interest point"""
    res = pd.DataFrame(columns=["lat_max", "lon_max", "lat_min", "lon_min", "route_id"])
    for i in np.array(df_rect.index):
        lat_max = np.float64(df_rect.loc[i]["lat_max"])
        # Obligation d'utiliser l'index car il existe plusieurs voyages pour le même trip_id (en fonction des différents réseaux)
        lon_max = np.float64(df_rect.loc[i]["lon_max"])
        lon_min = np.float64(df_rect.loc[i]["lon_min"])
        lat_min = np.float64(df_rect.loc[i]["lat_min"])
        try:
            # --- Etude cas 1 : coin inférieur gauche ---
            if lat <= lat_min and lon <= lon_min:
                if distance(lat, lon, lat_min, lon_min) < rayon:
                    res = pd.DataFrame.append(res, df_rect.loc[i])

                # --- Etude cas 2 : rectangle inférieur ---

            elif lat <= lat_min and lon >= lon_min and lon <= lon_max:
                if distance(lat, lon, lat_min, lon) <= rayon:
                    res = pd.DataFrame.append(res, df_rect.loc[i])

                # --- Etude cas 3 : coin inférieur droit ---

            elif lat <= lat_min and lon >= lon_max:
                if distance(lat, lon, lat_min, lon_max) <= rayon:
                    res = pd.DataFrame.append(res, df_rect.loc[i])

                # --- Etude cas 4 : rectangle gauche ---

            elif lat >= lat_min and lat <= lat_max and lon <= lon_min:
                if distance(lat, lon, lat, lon_min) <= rayon:
                    res = pd.DataFrame.append(res, df_rect.loc[i])

                # --- Etude cas 5 : rectangle central ---

            elif (
                lat >= lat_min and lat <= lat_max and lon >= lon_min and lon <= lon_max
            ):
                res = pd.DataFrame.append(res, df_rect.loc[i])

                # --- Etude cas 6 : rectangle droit ---

            elif lat >= lat_min and lat <= lat_max and lon >= lon_max:
                if distance(lat, lon, lat, lon_max) <= rayon:
                    res = pd.DataFrame.append(res, df_rect.loc[i])

                # --- Etude cas 7 : coin supérieur gauche ---

            elif lat >= lat_max and lon <= lon_min:
                if distance(lat, lon, lat_max, lon_min) <= rayon:
                    res = pd.DataFrame.append(res, df_rect.loc[i])

                # --- Etude cas 8 : rectangle supérieur ---

            elif lat >= lat_max and lon >= lon_min and lon <= lon_max:
                if distance(lat, lon, lat_max, lon) <= rayon:
                    res = pd.DataFrame.append(res, df_rect.loc[i])

                # --- Etude cas 9 : coin supérieur droit ---

            elif lat >= lat_max and lon >= lon_max:
                if distance(lat, lon, lat_max, lon_max) <= rayon:
                    res = pd.DataFrame.append(res, df_rect.loc[i])

        except:
            pass
    return res


def filter_stops_by_rect(df_stops, rect_cdt):
    boolean_mask = df_stops["route_id"].isin(rect_cdt)
    df_stops_filtered = df_stops[boolean_mask]

    df_stops_filtered.sort_values("stop_lat", inplace=True)
    return df_stops_filtered


def filter_stops(df_freq, rect_cdt, lat, lon):
    """Fonction qui permet d'affiner la recherche des arrêts - triés par latitude croissante - pour minimiser la complexité du programme"""
    filtered_stops = filter_stops_by_rect(df_freq, rect_cdt)

    filtered_lat = filtered_stops["stop_lat"]
    ni1, ni2 = 0, len(filtered_stops) - 1
    nj1, nj2 = 0, ni2
    i = ni2 // 2
    j = ni2 // 2

    lat_min = lat - marche_max / (6371 * 1e3)
    lat_max = lat + marche_max / (6371 * 1e3)

    while ni2 - ni1 > 1 or nj2 - nj1 > 1:
        if filtered_lat.iloc[i] >= lat_min:
            ni2 = i
        else:
            ni1 = i
        if filtered_lat.iloc[i] > lat_max:
            nj2 = j
        else:
            nj1 = j

        i = (ni1 + ni2) // 2
        j = (nj1 + nj2) // 2 + 1

    filtered_stops = filtered_stops.iloc[i:j]
    filtered_stops.sort_values("stop_lon", inplace=True)
    filtered_lon = filtered_stops["stop_lon"]

    lon_min = lon - marche_max / (6371 * 1e3) / np.sqrt(np.cos(lon * np.pi / 180))
    lon_max = lon + marche_max / (6371 * 1e3) / np.sqrt(np.cos(lon * np.pi / 180))

    ni1, ni2 = 0, len(filtered_stops) - 1
    nj1, nj2 = 0, ni2
    i = ni2 // 2
    j = ni2 // 2

    while ni2 - ni1 > 1 or nj2 - nj1 > 1:
        if filtered_lon.iloc[i] >= lon_min:
            ni2 = i
        else:
            ni1 = i
        if filtered_lon.iloc[i] > lon_max:
            nj2 = j
        else:
            nj1 = j

        i = (ni1 + ni2) // 2
        j = (nj1 + nj2) // 2 + 1

    filtered_stops = filtered_stops.iloc[ni1:nj2]

    return filtered_stops


def indicateur(df_freq, df_rect, lat, long):
    """Fonction de calcul de l'indicateur associé à UN point.

    Input : - CSV de fréquences généré par le module fréquence,
            - CSV de rectangles généré par le module rectangle,
            - latitude et longitude du point considéré.

    Output : - EDF ie. fréquence d'accès au transports en commun."""

    rect_candidates = rect_retenus(df_rect, lat, long, marche_max)[
        "route_id"
    ]  # calcul des rectangles retenus
    filtered_stops = filter_stops(
        df_freq, rect_candidates, lat, long
    )  # calcul des arrêts dont les latitudes sont acceptables. DataFrame triée par latitude croissante.

    array_EDF = np.empty((1, 2))
    n = len(filtered_stops)

    for i in range(n):
        # définir l'arrêt le plus proche en fonction de x, y et du route_id
        # ça implique d'avoir la distance_min associée à ce qu'on va appeler arret_proche
        stop_id, route_id, bus_per_hour, stop_lat, stop_long = filtered_stops.iloc[i]
        d = distance(lat, long, stop_lat, stop_long)
        if d < marche_max:
            temps_marche = (
                d / 75
            )  # je suppose que la vitesse moyenne d'un humain c'est 4,5km/h soit 75metre/min
            temps_attente_moy = 0.5 * 60 / bus_per_hour
            temps_acces_tot = temps_attente_moy + temps_marche
            EDF = 30 / temps_acces_tot
            array_EDF = np.vstack((array_EDF, [route_id, EDF]))

    df_EDF = pd.DataFrame(array_EDF[1:], columns=["route_id", "EDF"])

    if df_EDF.empty:
        return 0
    else:
        df_EDF.sort_values("EDF", inplace=True)
        df_EDF.drop_duplicates(["route_id"], keep="last", inplace=True)
        df_EDF.drop("route_id", axis=1, inplace=True)
        df_EDF = df_EDF.astype(float)
        EDF_max = df_EDF.iloc[-1]
        EDF_other = df_EDF[:-1].sum()
        return EDF_max + 0.5 * EDF_other
