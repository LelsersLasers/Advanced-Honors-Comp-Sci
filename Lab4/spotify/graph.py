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
import matplotlib.pyplot as plt
import numpy as np

import data


# ---------------------------------------------------------------------------- #
data_features = data.input_data_features(data.all_data(data.DataPath.SONG))


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
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
data_features_year = data.year_data()

x_axis = data_features_year["year"]
y_axises = data_features_year.columns[1:]

plt.figure()

for y_axis in y_axises:
	plt.plot(x_axis, data_features_year[y_axis], label=y_axis)
plt.title("Category Over Time")
plt.legend()
plt.show()
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
genres, data_features = data.genre_data()

x = np.arange(len(genres))
width = 0.035

fig, ax = plt.subplots()

for (i, (attribute, measurement)) in enumerate(data_features.items()):
    offset = width * (i - 4.5)
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects)

ax.set_title('Category Per Genre')
ax.set_xticks(x + width, genres)
ax.legend(loc='upper left', ncols=len(data_features))
ax.set_ylim(0, 1.1)

plt.show()
# ---------------------------------------------------------------------------- #