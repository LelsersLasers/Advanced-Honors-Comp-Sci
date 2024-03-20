import matplotlib.pyplot as plt

import data


def time_line_full(categories):
	categories.append("year")

	data_features_year = data.year_data()
	for category in data_features_year.columns:
		if category not in categories:
			data_features_year = data_features_year.drop(columns=category)

	x_axis = data_features_year["year"]
	y_axises = data_features_year.columns[1:]

	plt.figure()

	for y_axis in y_axises:
		plt.plot(x_axis, data_features_year[y_axis], label=y_axis)
	plt.title("Category Over Time")
	plt.legend()
	plt.show()