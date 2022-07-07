import pandas as pd

# Configurating the right path to data folder


def freq(df_agency, df_trips, df_stimes, df_stops, df_cal):

    agency_name = df_agency['agency_name'][0]
    df = pd.merge(df_trips, df_stimes, on="trip_id")[
        ["route_id", "service_id", "stop_id"]
    ]  # on associe les trips et les arrêts

    #if df_cal == None:
    df = df.groupby(
        ["route_id", "stop_id"], as_index=False
    ).size()  # on calcule le nombre de bus qui passe par jour
    df["bus_per_week"] = (
        df["size"] * 7
    )  # dont on déduit un nombre moyen de bus par heure, pondéré par le nombre de jours de service
    df = df.groupby(["route_id", "stop_id"], as_index=False).sum()
    df["bus_per_hour"] = df["size"] / 12
    df.drop(labels=["size", "bus_per_week"], axis=1, inplace=True)
    df = pd.merge(
        df, df_stops[["stop_id", "stop_lat", "stop_lon"]], on="stop_id"
    )  # on ajoute les coordonnées des arrêts
    df['agency_name'] = pd.DataFrame([agency_name for k in range(len(df))])
    # else:
    #     print('here')
    #     df_cal["nb_days"] = df_cal.iloc[:, 1:].sum(
    #         axis=1
    #     )  # on calcule le nombre de jours où le trip est effectué dans la semaine
    #     df_cal = df_cal[["service_id", "nb_days"]]
    #     df = pd.merge(df, df_cal, on="service_id")  # puis on l'ajoute à la dataframe

    #     df = df.groupby(
    #         ["route_id", "stop_id", "nb_days"], as_index=False
    #     ).size()  # on calcule le nombre de bus qui passe par jour
    #     df["bus_per_week"] = (
    #         df["size"] * df["nb_days"]
    #     )  # dont on déduit un nombre moyen de bus par heure, pondéré par le nombre de jours de service
    #     df = df.groupby(["route_id", "stop_id"], as_index=False).sum()
    #     df["bus_per_hour"] = df["size"] * df["nb_days"] / (7 * 12)
    #     df.drop(labels=["nb_days", "size", "bus_per_week"], axis=1, inplace=True)
    #     df = pd.merge(
    #         df, df_stops[["stop_id", "stop_lat", "stop_lon"]], on="stop_id"
    #     )  # on ajoute les coordonnées des arrêts
    #     df['agency_name'] = pd.DataFrame([agency_name for k in range(len(df))])

    return df