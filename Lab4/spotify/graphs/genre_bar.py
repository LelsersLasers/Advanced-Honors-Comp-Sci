import matplotlib.pyplot as plt
import numpy as np

import data


def genre_bar_full(categories):
	categories.append("genre")

	genres, data_features = data.genre_data()
	keys = list(data_features.keys())
	for key in keys:
		if key not in categories:
			data_features.pop(key)

	x = np.arange(len(genres))
	width = 0.035

	_fig, ax = plt.subplots()

	overall_offset = len(data_features.keys()) / 2 - 1.5

	for (i, (attribute, measurement)) in enumerate(data_features.items()):
		offset = width * (i - overall_offset)
		rects = ax.bar(x + offset, measurement, width, label=attribute)
		ax.bar_label(rects)

	ax.set_title('Category Per Genre')
	ax.set_xticks(x + width, genres)
	ax.legend(loc='upper left', ncols=len(data_features))
	ax.set_ylim(0, 1.1)

	plt.show()