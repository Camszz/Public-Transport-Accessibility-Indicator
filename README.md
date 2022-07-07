# ue22-Projet
 School project about building a indicator of accessibility for public transport in collaboration with the Rhône-Alpes region

## 1. Data-builder

Put the GTFS files you want to work on in the **DATA folder** and start **"DATA_builder.py"**. It will create the .csv files the program needs to run. For each Dataset you just have to do it once : when the data is built you can get rid of the .csv files.

## 2. Indicator program

Put a .csv file containing the latitudes and longitudes in the main folder. The file should follow this scheme :

*latitude 1, longitude 1 <br/>
latitude 2, longitude 2 <br/>
... <br/>
latitude n, longitude n*. <br/>

In the current version you **must not put columns names** at the top of the .csv file.

Start *program.py*, type the *yourfilename.csv* when asked. The file with the indicator will be saved as *AI_yourfilename.csv* - *AI* stands for Accessibility Indicator.

Scheme of the output file will be the following :

*lat, long, AI <br/>
latitude 1, longitude 1, AI 1 <br/>
... <br/>
latitude n, longitude n, AI n*.

## Note on the AI

Usual PTAL ranking is 1a, 1b, 2, 3, 4, 5, 6a, 6b with 6b being the best and 1a the worst. To keep numbers only we decided that **1a=0.8, 1b=1.2, 6a=5.8, 6b=6.2**.

## Map generator

You can generate a map background of chosen resolution in the *carte.py* file, you just have to enter the desired DPI resolution.

Once the map is generated, you have to run *testing_map.py* (still in Beta version) which should return an array of AIs. The *plot.py* file is used to... plot the above-mentionned array.