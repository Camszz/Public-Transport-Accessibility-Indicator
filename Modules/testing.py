import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indicator

df_freq = pd.read_csv('freq.csv')
ma_carte = np.fromfile('cartographie/ma_carte')
ma_carte = np.reshape(ma_carte, (217,335,3))

EDF_array = indicator.map_indicator(df_freq, ma_carte)
n,m, p = ma_carte.shape
for i in range(n) :
    for j in range(m) :
        if ma_carte[i, j, 0] == 0 :
            EDF_array[i, j] = -10

plt.imshow(EDF_array)
plt.colorbar()
plt.show()
