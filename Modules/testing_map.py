from tracemalloc import start
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indicator
import time

df_freq = pd.read_csv('freq.csv')
ma_carte = np.load('cartographie/ma_carte.npy')

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

start_time = time.time()
EDF_array = indicator.map_indicator(df_freq, ma_carte)
n,m, p = ma_carte.shape

PTAL_array = np.empty((n, m))
for i in range(n) :
    for j in range(m) :
        if ma_carte[i, j, 0] == 0 :
            PTAL_array[i, j] = -1
        else :
            PTAL_array[i, j] = EDF_to_PTAL(EDF_array[i, j])
stop_time = time.time()

print(stop_time-start_time)

np.save('cartographie/indicator_map', PTAL_array)

# cMap = ['white', 'navy', 'blue', 'turquoise', 'mediumseagreen', 'yellow', 'orange', 'red', 'darkred']
# plt.imshow(PTAL_array, cmap=cMap)
# plt.title("Carte d'accessibilité aux transports en commun - Région Rhône-Alpes")
# plt.colorbar()
# plt.show()