import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import indicator


df_freq = pd.read_csv("freq.csv")
df_rect = pd.read_csv("rectangles.csv")

ma_carte = np.fromfile("cartographie/ma_carte")

ma_carte = np.reshape(ma_carte, (217, 335, 3))

rendu_final = np.zeros(ma_carte.shape)

for i in range(0, rendu_final.shape[0], 20):
    for j in range(0, rendu_final.shape[1], 20):
        if ma_carte[i, j, 0] == 1:
            rendu_final[i, j] = indicator.indicateur(
                df_freq, df_rect, ma_carte[i, j, 1], ma_carte[i, j, 2]
            )

plt.imshow(rendu_final[::20, ::20])
plt.colorbar()
plt.show()