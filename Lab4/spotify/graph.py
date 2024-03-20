# - Correlation between categories
# 	- Input: (method)
# 	- Output: (heat map)
# - Average (mean? median?) category over time
# 	- Input: (categories)
# 	- Output: (line graph)
# - Average (mean? median?) category per genre
# 	- Input: (categories)
# 	- Output: (bar graph)


# valence,year,acousticness,artists,danceability,duration_ms,energy,explicit,id,instrumentalness,key,liveness,loudness,mode,name,popularity,release_date,speechiness,tempo
import data
data_features = data.input_data_features(data.all_data(data.DataPath.SONG))

import matplotlib.pyplot as plt
import numpy as np

class Correlations:
	PEARSON  = "pearson"
	KENDALL  = "kendall"
	SPEARMAN = "spearman"


def correlations(data_features, method):
	print(f"\nCalculating {method} correlations...")
	corr = data_features.corr(method)
	corr = np.asarray(corr)
	print("Correlations calculated\n")
	return corr

def heat_map(corr, method):
	fig = plt.figure(figsize=(8, 8))
	plt.title(f"{method.upper()} Correlation Heat Map")
	plt.imshow(corr, cmap='plasma', origin='upper')
	plt.xticks(range(len(data_features.columns)), data_features.columns, rotation=90)
	plt.yticks(range(len(data_features.columns)), data_features.columns)
	fig.tight_layout()
	plt.colorbar()
	plt.show()

corr = correlations(data_features, Correlations.PEARSON)
heat_map(corr, Correlations.PEARSON)