import matplotlib.pyplot as plt

import graphs.save_graph
import data

SAVE_PATH = "output/temp/time_line-"

def time_line_full(categories, id=None):
    categories.append("year")

    data_features_year = data.year_data()
    for category in data_features_year.columns:
        if category not in categories:
            data_features_year = data_features_year.drop(columns=category)

    x_axis = data_features_year["year"]
    y_axises = data_features_year.columns[1:]

    plt.figure(figsize=(10, 8))

    for y_axis in y_axises:
        plt.plot(x_axis, data_features_year[y_axis], label=y_axis)
    plt.title("Category Over Time")
    plt.legend()

    if id is not None:
        return graphs.save_graph.graph_to_b64(id, SAVE_PATH)
    else:
        return None

    