"""
    Description: Plot training history from a .json file.
    Author: Millan Kumar
    Date: 1/24/2024
"""

import argparse

ap = argparse.ArgumentParser()

ap.add_argument(
    "-p",
    "--plot-history-load-path",
    required=True,
    help="path (.json) to load training history from",
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
import json
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

    print("lens", len(lst), len(rolling))
    return rolling


try:
	with open(args["plot_history_load_path"], "r") as f:
		history = json.load(f)
except FileNotFoundError:
	ap.error("invalid path to training history file")


train_accuracy_axis = history['accuracy']

validation_accuracy_axis_base = history['val_accuracy']
if args["window_size"] > 1:
    validation_accuracy_axis = convert_to_rolling(validation_accuracy_axis_base, args["window_size"])
else:
    validation_accuracy_axis = validation_accuracy_axis_base

train_loss_axis = history['loss']

validation_loss_axis_base = history['val_loss']
if args["window_size"] > 1:
    validation_loss_axis = convert_to_rolling(validation_loss_axis_base, args["window_size"])
else:
    validation_loss_axis = validation_loss_axis_base

epoch_axis = range(1, len(train_accuracy_axis) + 1)

plt.plot(epoch_axis, train_accuracy_axis, 'b', label='training accuracy')
plt.plot(epoch_axis, validation_accuracy_axis, 'r', label='validation accuracy')
plt.title('Accuracy')
plt.legend()

plt.figure()
plt.plot(epoch_axis, train_loss_axis, 'b', label='training loss')
plt.plot(epoch_axis, validation_loss_axis, 'r', label='validation loss')
plt.title('Loss')
plt.legend()

plt.show()