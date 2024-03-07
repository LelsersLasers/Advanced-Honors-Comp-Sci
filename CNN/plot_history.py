"""
    Description: Plot training history from a .json file.
    Author: Millan Kumar
    Date: 3/7/2024
"""

import argparse

ap = argparse.ArgumentParser()

ap.add_argument(
    "-p",
    "--plot-history-load-path",
    required=True,
    help="path (.csv) to load training history from",
)
ap.add_argument(
    "-w",
    "--window-size",
    required=False,
    help="size of window for rolling accuracy/loss for validation",
    default=3,
    type=int,
)

args = vars(ap.parse_args())
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import csv
import matplotlib.pyplot as plt


def convert_to_rolling(lst, size):
    slice_size_lower = size // 2
    slice_size_upper = size - slice_size_lower

    rolling = []
    max_len = len(lst)
    for i in range(max_len):
        lower = max(0, i - slice_size_lower)
        upper = min(max_len, i + slice_size_upper)

        total = sum(lst[lower:upper])
        count = upper - lower
        rolling.append(total / count)

    return rolling


try:
    history = {}
    with open(args["plot_history_load_path"], "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key, value in row.items():
                if key not in history:
                    history[key] = []
                history[key].append(float(value))
except FileNotFoundError:
    ap.error("invalid path to training history file")


epoch_axis = range(1, len(history["epoch"]) + 1)

axis_pairs = []
for key, value in history.items():
    if key == "epoch" or key.startswith("val_"):
        continue
    axis_pairs.append((key, f"val_{key}"))

for (train_axis_label, val_axis_label) in axis_pairs:
    plt.figure()

    train_axis = convert_to_rolling(history[train_axis_label], args["window_size"])
    val_axis = convert_to_rolling(history[val_axis_label], args["window_size"])

    plt.plot(epoch_axis, train_axis, 'b', label=train_axis_label)
    plt.plot(epoch_axis, val_axis,   'r', label=val_axis_label)
    plt.title(train_axis_label)
    plt.legend()

plt.show()