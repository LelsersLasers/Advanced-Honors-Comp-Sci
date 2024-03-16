import numpy as np
np.set_printoptions(precision=3, suppress=True)

# import tensorflow as tf
import tensorflow.keras as keras
import tensorflow_similarity as tfsim



model = keras.models.load_model(
	"output/try1-fullsave",
	custom_objects={"SimilarityModel": tfsim.models.SimilarityModel},
)


# valence,year,acousticness,artists,danceability,duration_ms,energy,explicit,id,instrumentalness,key,liveness,loudness,mode,name,popularity,release_date,speechiness,tempo
# test='0.606,2009,0.00244,["Rascal Flatts"],0.562,276707,0.91,0,5YbeJyTQkdSAWe1Ie4sLAl,0.0,5,0.0676,-6.939,1,"Life is a Highway - From ""Cars""",56,2009-01-01,0.058,103.057'
test = '0.899,1926,0.995,["Louis Armstrong & His Hot Five"],0.614,189333,0.196,0,0jiH6Bf3OOm36ubMWZ0Sr5,0.892,4,0.0526,-14.019,1,Jazz Lips,9,1926,0.4270000000000001,201.11900000000003'

test = test.split(',')


valence = float(test[0])
year = float(test[1])
acousticness = float(test[2])
danceability = float(test[4])
duration_ms = float(test[5])
energy = float(test[6])
instrumentalness = float(test[9])
key = float(test[10])
liveness = float(test[11])
loudness = float(test[12])
speechiness = float(test[17])
tempo = float(test[18])

x = np.array([valence, year, acousticness, danceability, duration_ms, energy, instrumentalness, key, liveness, loudness, speechiness, tempo], dtype=np.float32)
x = np.expand_dims(x, axis=0)
print(x)

closest = model.lookup(x, k=500)

print(closest)