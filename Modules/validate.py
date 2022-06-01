#reading module for GTFS files
import gtfs_kit as gk

path = Path("D:/camdu/Google Drive/Scolaire/Mines/ue22 - Ingénierie Logicielle/ue22-Projet/DATA")

feed = (gk.read_feed(path, dist_units='km'))

gk.validate()