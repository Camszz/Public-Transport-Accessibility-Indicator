import indicator
import numpy as np
import pandas as pd

name = input("enter the .csv file name \n")
df_coord = pd.read_csv(name, names=['lat', 'long'])
arr_coord = df_coord.to_numpy()
arr_PTAL = np.empty((0))

df_freq = pd.read_csv("freq.csv")
df_rectangles = pd.read_csv("rectangles.csv")

def EDF_to_PTAL(EDF) :
    if EDF < 2.5 : PTAL = 0.8
    elif EDF < 5 : PTAL = 1.2
    elif EDF < 10 : PTAL = 2
    elif EDF < 15 : PTAL = 3
    elif EDF < 20 : PTAL = 4
    elif EDF < 25 : PTAL = 5
    elif EDF < 40 : PTAL = 5.8
    else : PTAL = 6.2
    return PTAL

for coord in arr_coord:
    lat, long = coord[0], coord[1]
    EDF = indicator.indicateur(df_freq, df_rectangles, lat, long)
    PTAL = EDF_to_PTAL(EDF)
    arr_PTAL = np.append(arr_PTAL, PTAL)

df_coord['AI'] = arr_PTAL

df_coord.to_csv('AI_'+name+'.csv', index = False)