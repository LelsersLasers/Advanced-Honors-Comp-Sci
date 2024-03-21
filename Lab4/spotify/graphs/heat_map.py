import matplotlib.pyplot as plt
import numpy as np

import data


def correlations(data_features, method):
	print(f"\nCalculating {method} correlations...")
	corr = data_features.corr(method)
	corr = np.asarray(corr)
	print("Correlations calculated\n")
	return corr

def heat_map(corr, data_features, method):
	fig, ax = plt.subplots()
	fig.set_figwidth(10)
	fig.set_figheight(8)

	plt.title(f"{method.upper()} Correlation Heat Map")
	plt.imshow(corr, cmap='plasma', origin='upper')

	plt.xticks(range(len(data_features.columns)), data_features.columns, rotation=90)
	plt.yticks(range(len(data_features.columns)), data_features.columns)

	for (i, j), val in np.ndenumerate(corr):
		ax.text(j, i, f"{val:.2f}", ha='center', va='center', color='black')

	fig.tight_layout()
	plt.colorbar()
	plt.show()

def full_heat_map(categories, method):
	data_features = data.input_data_features(data.all_data(data.DataPath.SONG))
	for category in data_features.columns:
		if category not in categories:
			data_features = data_features.drop(columns=category)

	corr = correlations(data_features, method)
	heat_map(corr, data_features, method)