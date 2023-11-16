import argparse

ap = argparse.ArgumentParser()

ap.add_argument(
    "-p",
    "--plot-history-load-path",
    required=True,
    help="path (.json) to load training history from",
)

args = vars(ap.parse_args())
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import json
import matplotlib.pyplot as plt


try:
	with open(args["plot_history_load_path"], "r") as f:
		history = json.load(f)
except FileNotFoundError:
	ap.error("invalid path to training history file")


print(f"{history=}")

train_accuracy_axis = history['accuracy']
validation_accuracy_axis = history['val_accuracy']
train_loss_axis = history['loss']
validation_loss_axis = history['val_loss']

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