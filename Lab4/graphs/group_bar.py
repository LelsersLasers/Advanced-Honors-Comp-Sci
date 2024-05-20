import matplotlib.pyplot as plt
import numpy as np

import graphs.save_graph
import data


SAVE_PATH = "output/temp/bar-"


def bar_full(categories, group, id=None):
    categories.append(group)

    groups, data_features = data.artist_data() if group == "artists" else data.genre_data()
    keys = list(data_features.keys())
    for key in keys:
        if key not in categories:
            data_features.pop(key)

    x = np.arange(len(groups))
    width = 0.05

    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    fig.set_figheight(8)

    overall_offset = len(data_features.keys()) / 2 - 1.5

    for (i, (attribute, measurement)) in enumerate(data_features.items()):
        offset = width * (i - overall_offset)
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects)

    title = f"Category per {group.capitalize()}"
    ax.set_title(title)

    ax.set_xticks(x + width, groups)
    ax.legend(loc='upper left', ncols=len(data_features))
    ax.set_ylim(0, 1.1)

    if id is not None:
        save_path = SAVE_PATH + group + "-"
        return graphs.save_graph.graph_to_b64(id, save_path)
    else:
        return None