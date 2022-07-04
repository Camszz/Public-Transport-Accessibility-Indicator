import indicator
import numpy as np
import pandas as pd

arr_coord = np.array([[45.188529, 5.724524]])
arr_EDF = np.empty((0))

df_freq = pd.read_csv("freq.csv")
df_rectangles = pd.read_csv("rectangles.csv")

for coord in arr_coord :
    lat, long = coord[0], coord[1]
    EDF = indicator.indicateur(df_freq, df_rectangles, lat, long)
    arr_EDF = np.append(arr_EDF, EDF)

print(arr_EDF)