import json
import numpy as np
import matplotlib.pyplot as plt

#On obtient les coordonées géographiques de la région Auvergne Rhône-Alpes sur https://france-geojson.gregoiredavid.fr/

DPI = 500

def carte():

    with open('cartographie/data.json') as mon_fichier:
        data = json.load(mon_fichier)

    contours = data['geometry']['coordinates']


    c1, c2 = contours  #il y a deux contours car il y a une enclave dans la région
    contour_region = np.array(c1)
    contour_enclave = np.array(c2)

    longitude_min = min(contour_region[:,0])
    longitude_max = max(contour_region[:,0])
    latitude_min = min(contour_region[:,1])
    latitude_max = max(contour_region[:,1])

    #On plot la région avec un plt.fill pour avoir l'interieur des contours en noir puis on sauvegarde l'image pour en faire un masque

    plt.fill(contour_region[:,0], contour_region[:,1], c='black')
    plt.fill(contour_enclave[:,0], contour_enclave[:,1], c='white')

    plt.xlim([longitude_min, longitude_max])
    plt.ylim([latitude_min, latitude_max])

    plt.axis('off')

    plt.savefig('cartographie/out.jpg', dpi=DPI, bbox_inches = None) #le paramètre dpi "dot per inch" nous permet de choisir la résolution de l'image !!

    #Création du masque

    im = plt.imread('cartographie/out.jpg')[:, :, 0]
    im_mask = (im < 127)

    #Rogner le masque :

    compt_ligne = 0

    def test_ligne(a):
        only_false = True
        i=0
        while only_false == True and i<len(a):
            if a[i] == True:
                only_false = False
            i+=1
        return only_false

    for j in range(im_mask.shape[0]):
        if test_ligne(im_mask[j]):
            compt_ligne+=1

    a = np.zeros((im_mask.shape[0]-compt_ligne, im_mask.shape[1]))

    i = 0
    j = 0
    for i in range(im_mask.shape[0]):
        if not(test_ligne(im_mask[i])):
            a[j] = im_mask[i]
            j+=1

    compt_colonne = 0

    for j in range(im_mask.shape[1]):
        if test_ligne(im_mask[:,j]):
            compt_colonne+=1


    im_crop = np.zeros((im_mask.shape[0]-compt_ligne, im_mask.shape[1]-compt_colonne))

    i = 0
    j = 0
    for i in range(a.shape[1]):
        if not(test_ligne(a[:,i])):
            im_crop[:,j] = a[:,i]
            j+=1


    #Création du tableau des coordonnées géographiques

    nb_lignes = im_crop.shape[0]
    nb_col = im_crop.shape[1]

    latitudes = np.linspace(latitude_min, latitude_max, nb_lignes)  #ON DEVRAIT PRENDRE EN COMPTE L ANGLE MAIS EN PREMIERE APPROXIAMATION CA PASSE !
    longitudes = np.linspace(longitude_min, longitude_max, nb_col)

    coords = np.zeros((nb_lignes, nb_col, 2))

    for i in range(nb_lignes):
        for j in range(nb_col):
            coords[i,j,0] = longitudes[j]
            coords[i,j,1] = latitudes[-i-1]

    new_im_crop = np.reshape(im_crop, (nb_lignes, nb_col, 1))

    map_finale = np.concatenate((new_im_crop, coords), axis=2) #On concatene new_im_crop dont les "cases" valent 0 ou 1 selon si on est dans la région et coords qui contient les coords, ce qui donne un tableau qui renseigne les coords geographique et la présence dans la region 

    np.save('cartographie/ma_carte', map_finale)

    return(map_finale)

carte()





