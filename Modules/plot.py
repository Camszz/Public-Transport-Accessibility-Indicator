from cProfile import label
import matplotlib.pyplot as plt
import numpy as np

PTAL_array = np.load('cartographie/indicator_map.npy')

cMap = ['white', 'navy', 'blue', 'turquoise', 'mediumseagreen', 'yellow', 'orange', 'red', 'darkred']
plt.imshow(PTAL_array)
plt.title("Carte d'accessibilité aux transports en commun - Région Rhône-Alpes")
plt.axis('off')
clb = plt.colorbar()
clb.ax.set_title('AI')
plt.legend()
plt.show()