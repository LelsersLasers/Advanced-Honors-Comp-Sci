import matplotlib.pyplot as plt
import numpy as np

import data


def bar_full(categories, group):
	categories.append(group)

	groups, data_features = data.artist_data() if group == "artists" else data.genre_data()
	print(groups)
	keys = list(data_features.keys())
	for key in keys:
		if key not in categories:
			data_features.pop(key)

	x = np.arange(len(groups))
	width = 0.05

	_fig, ax = plt.subplots()

	overall_offset = len(data_features.keys()) / 2 - 1.5

	for (i, (attribute, measurement)) in enumerate(data_features.items()):
		offset = width * (i - overall_offset)
		rects = ax.bar(x + offset, measurement, width, label=attribute)
		ax.bar_label(rects)

	title = f'Category per {group.capitalize()}'
	ax.set_title(title)

	ax.set_xticks(x + width, groups)
	ax.legend(loc='upper left', ncols=len(data_features))
	ax.set_ylim(0, 1.1)

	plt.show()