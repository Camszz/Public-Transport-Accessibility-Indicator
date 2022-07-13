import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'

marche_max = 1500


def distance(lat_a, lon_a, lat_b, lon_b):
    """Fonction retournant la distance entre deux points à la surface de la Terre"""
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
    res = pd.DataFrame(columns=["lat_max", "lon_max", "lat_min", "lon_min", "route_id", "agency_name"])
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
                    #res = pd.DataFrame.append(res, df_rect.loc[i])
                    res.loc[len(res), res.columns] = df_rect.loc[i]

                # --- Etude cas 2 : rectangle inférieur ---

            elif lat <= lat_min and lon >= lon_min and lon <= lon_max:
                if distance(lat, lon, lat_min, lon) <= rayon:
                    #res = pd.DataFrame.append(res, df_rect.loc[i])
                    res.loc[len(res), res.columns] = df_rect.loc[i]

                # --- Etude cas 3 : coin inférieur droit ---

            elif lat <= lat_min and lon >= lon_max:
                if distance(lat, lon, lat_min, lon_max) <= rayon:
                    #res = pd.DataFrame.append(res, df_rect.loc[i])
                    res.loc[len(res), res.columns] = df_rect.loc[i]

                # --- Etude cas 4 : rectangle gauche ---

            elif lat >= lat_min and lat <= lat_max and lon <= lon_min:
                if distance(lat, lon, lat, lon_min) <= rayon:
                    #res = pd.DataFrame.append(res, df_rect.loc[i])
                    res.loc[len(res), res.columns] = df_rect.loc[i]

                # --- Etude cas 5 : rectangle central ---

            elif (
                lat >= lat_min and lat <= lat_max and lon >= lon_min and lon <= lon_max
            ):
                #res = pd.DataFrame.append(res, df_rect.loc[i])
                res.loc[len(res), res.columns] = df_rect.loc[i]

                # --- Etude cas 6 : rectangle droit ---

            elif lat >= lat_min and lat <= lat_max and lon >= lon_max:
                if distance(lat, lon, lat, lon_max) <= rayon:
                    #res = pd.DataFrame.append(res, df_rect.loc[i])
                    res.loc[len(res), res.columns] = df_rect.loc[i]

                # --- Etude cas 7 : coin supérieur gauche ---

            elif lat >= lat_max and lon <= lon_min:
                if distance(lat, lon, lat_max, lon_min) <= rayon:
                    #res = pd.DataFrame.append(res, df_rect.loc[i])
                    res.loc[len(res), res.columns] = df_rect.loc[i]

                # --- Etude cas 8 : rectangle supérieur ---

            elif lat >= lat_max and lon >= lon_min and lon <= lon_max:
                if distance(lat, lon, lat_max, lon) <= rayon:
                    #res = pd.DataFrame.append(res, df_rect.loc[i])
                    res.loc[len(res), res.columns] = df_rect.loc[i]

                # --- Etude cas 9 : coin supérieur droit ---

            elif lat >= lat_max and lon >= lon_max:
                if distance(lat, lon, lat_max, lon_max) <= rayon:
                    #res = pd.DataFrame.append(res, df_rect.loc[i])
                    res.loc[len(res), res.columns] = df_rect.loc[i]

        except:
            pass
    return res


def filter_stops_by_rect(df_stops, rect_cdt):
    """Fonction retournant la liste des arrêts contenus dans les rectangles sélectionnés
    
    Input : - DataFrame des arrêts
            - DataFrame des rectangles retenus
    
    Output : - DataFrame des arrêts candidats"""
    boolean_mask = df_stops["route_id"].isin(rect_cdt)
    df_stops_filtered = df_stops[boolean_mask]

    return df_stops_filtered


def filter_stops(df_freq, rect_cdt, lat, lon):
    """Fonction qui permet d'affiner la recherche des arrêts - triés par latitude croissante - pour minimiser la complexité du programme"""
    filtered_stops = filter_stops_by_rect(df_freq, rect_cdt)

    filtered_lat = filtered_stops["stop_lat"]
    ni1, ni2 = 0, len(filtered_stops) - 1
    nj1, nj2 = 0, ni2
    i = ni2 // 2
    j = ni2 // 2

    lat_min = lat - 180*marche_max/(6371*1e3)/np.pi
    lat_max = lat + 180*marche_max/(6371*1e3)/np.pi

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

    lon_min = lon - 180*marche_max/(6371*1e3)/np.sqrt(np.cos(lon*np.pi/180))/np.pi
    lon_max = lon + 180*marche_max/(6371*1e3)/np.sqrt(np.cos(lon*np.pi/180))/np.pi

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

    rect_candidates = rect_retenus(df_rect, lat, long, marche_max)['route_id'] #calcul des rectangles retenus
    filtered_stops = filter_stops_by_rect(df_freq, rect_candidates) #et des arrêts contenus dedans


    array_EDF = np.empty((1, 2)) #initialisation du tableau des EDF
    n = len(filtered_stops)

    for i in range(n): #on parcourt l'ensemble des arrêts contenus dans les rectangles
        agency_name, stop_id, route_id, bus_per_hour, stop_lat, stop_long = filtered_stops.iloc[i]
        d = distance(lat, long, stop_lat, stop_long)
        if d < marche_max: #si la distance à l'arrêt est plus petite qu'une certaine distance limite, on calcule son EDF
            temps_marche = (
                d / 75
            )  # on suppose que la vitesse moyenne d'un humain est 4,5km/h soit 75metre/min
            temps_attente_moy = 0.5 * 60 / bus_per_hour
            temps_acces_tot = temps_attente_moy + temps_marche
            EDF = 30 / temps_acces_tot #ces calculs ci sont issus de la note méthodologique
            array_EDF = np.vstack((array_EDF, [route_id, EDF])) #on ajoute le nouvel EDF - même si la route est déjà prise en compte
            
    df_EDF = pd.DataFrame(array_EDF[1:], columns=["route_id", "EDF"]) #on enlève la première ligne qui était issue du np.empty

    if df_EDF.empty: #deux cas de figure : soit tous les arrêts étaient trop loin (cas 1)...
        return 0 
    else: #soit certains étaient assez proche et on a calculé des EDF (cas 2)
        df_EDF.sort_values("EDF", inplace=True) #on trie la DataFrame par EDF croissante...
        df_EDF.drop_duplicates(["route_id"], keep="last", inplace=True) #ce qui permet de ne garder que le plus grand EDF de chaque route_id
        df_EDF.drop("route_id", axis=1, inplace=True)
        df_EDF = df_EDF.astype(float)
        EDF_max = df_EDF.iloc[-1] #on récupère l'EDF le plus grand
        EDF_other = df_EDF[:-1].sum() #il ne reste plus qu'à sommer avec une pondération de 0.5 les EDF plus petits
        return (EDF_max + 0.5*EDF_other)[0]
    
def map_indicator(df_freq, coord_array) :
    """Fonction renvoyant un array d'EDF_totaux
    
    Input : - DataFrame de fréquences
            - Tableau de coordonées
    
    Output : - Tableau des EDF correspondantes"""
    
    n,m, p = coord_array.shape #on récupère les dimensions du tableau en entrée
    EDF_list = [[0 for k in range(m)] for j in range(n)] #et on initialise une liste de liste dans laquelle on mettra les DataFrame d'EDF
    notnull_array = np.zeros((n,m)) #ce tableau permettra de récupérer les cases non nulles pour ne pas avoir de complexité en n*m

    for k in range(n) :
        for j in range(m):
            EDF_list[k][j] = np.empty((1, 2)) #initialisation des DataFrame
    res = np.zeros((n, m)) #et initialisation du tableau de retour

    lat_max, lat_min = coord_array[0,0,2], coord_array[n-1, 0, 2] #on récupère des éléments géographiques sur le tableau
    long_min, long_max = coord_array[0,0,1], coord_array[0, m-1, 1]
    Delta_lat, Delta_long = lat_max-lat_min, long_max-long_min
    d_lat, d_long = Delta_lat/n, Delta_long/m
    R_case = max(distance(lat_min, long_min, lat_min, long_min+d_long), distance(lat_min, long_min, lat_min+d_lat, long_min)) #on calcule le rayon d'une case de tableau
    i_close_cases, j_close_cases = int(marche_max/(6371*1e3)/np.sqrt(np.cos(d_long*np.pi/180))/d_long)+1, int(marche_max/(6371*1e3)/d_lat)+1 #et on détermine le nombre de cases qu'il faudra regarder autour de chaque arrêt 

    for ind in df_freq.index : #on parcourt les arrêts et on va distribuer les EDF aux cases du tableau environnantes
        agency_name, stop_id, route_id, bus_per_hour, stop_lat, stop_long = df_freq.iloc[ind]
        i, j = int((stop_long-long_min)/d_long), int((lat_max-stop_lat)/d_lat)
        for d_i in range(-i_close_cases, +i_close_cases+1) :
            for d_j in range(-j_close_cases, +j_close_cases+1) :
                try : #le try permet d'éviter les out of range et de ne pas créer de cas spécifique pour les bords du tableau
                    inside, long, lat = coord_array[j+d_j, i+d_i]
                    d = distance(lat,long, stop_lat, stop_long)
                    d = max(0, d-R_case) #on considère que si on est dans une case la distance est nulle, sinon on prend la plus petite distance possible à la case (d'où le R_case)
                    if d < marche_max and bus_per_hour != 0 and inside==1: #même calcul que pour l'indicateur non-vectorisé
                        temps_marche = d/75
                        temps_attente_moy = 0.5 * 60 / bus_per_hour
                        temps_acces_tot = temps_attente_moy + temps_marche
                        EDF = 30/temps_acces_tot
                        EDF_list[j+d_j][i+d_i] = np.vstack((EDF_list[j+d_j][i+d_i], [route_id, EDF]))
                        notnull_array[j+d_j, i+d_i] += 1 #on ajoute juste l'information que la case (j+dj, i+di) a un EDF non nul
                except :
                    pass

    notnull_array = np.nonzero(notnull_array) #on récupère les EDF non nuls
    for k in range(len(notnull_array[0])) : #puis on calcule pour chaque point le EDF_total
        i, j = notnull_array[0][k], notnull_array[1][k]
        array_EDF = np.copy(EDF_list[i][j])
        df_EDF = pd.DataFrame(array_EDF[1:], columns=["route_id", "EDF"])
        if df_EDF.empty :
            res[i, j] = 0
        else :
            df_EDF.sort_values("EDF", inplace=True)
            df_EDF.drop_duplicates(["route_id"], keep = "last", inplace=True)
            df_EDF.drop("route_id", axis=1, inplace=True)
            df_EDF = df_EDF.astype(float)
            EDF_max = df_EDF.iloc[-1]
            EDF_other = df_EDF[:-1].sum()
            res[i, j] = EDF_max + 0.5*EDF_other

    return res