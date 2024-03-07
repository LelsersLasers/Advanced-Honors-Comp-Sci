"""
    Description: Custom CNN for weather classification.
    Author: Millan Kumar
    Date: 3/7/2024
"""

import argparse

ap = argparse.ArgumentParser()

ap.add_argument(
    "-e",
    "--epochs",
    required=True,
    help="number of epochs to train for",
    type=int,
)
ap.add_argument(
    "-k",
    "--top-k-categorical-accuracy",
    required=False,
    help="top k categorical accuracy metric",
    default=2,
    type=int,
)
ap.add_argument(
    "-r",
    "--learning-rate",
    required=False,
    help="learning rate for optimizer",
    default=0.0001,
    type=float,
)
ap.add_argument(
	"-g",
	"--decay-rate",
	required=False,
	help="decay rate for learning rate",
	default=0.9,
	type=float,
)
ap.add_argument(
	"-j",
	"--decay-steps",
	required=False,
	help="decay steps for learning rate",
	default=400,
	type=int,
)
ap.add_argument(
	"-m",
	"--l1",
	required=False,
	help="l1 regularization for all layers",
	default=0.2,
	type=float,
)
ap.add_argument(
	"-n",
    "--l2",
    required=False,
    help="l2 regularization for all layers",
    default=0.2,
    type=float,
)
ap.add_argument(
    "-l",
    "--load-checkpoint-path",
    required=False,
    help="checkpoint to load model weights from",
    default=None,
)
ap.add_argument(
    "-c",
    "--checkpoint-save-path",
    required=False,
    help="location to save model checkpoint to after every epoch",
    default=None,
)
ap.add_argument(
    "-f",
    "--frequency-checkpoint",
    required=False,
    help="frequency of saving model checkpoint (in epochs)",
    default=1,
    type=int
)
ap.add_argument(
    "-s",
    "--save-path",
    required=False,
    help="location to save model after training",
    default=None,
)
ap.add_argument(
    "-p",
    "--plot-history-save-path",
    required=False,
    help="path (.csv) to save training history to (will append if file exists)",
    default=None,
)
ap.add_argument(
    "-d",
    "--dropout",
    required=False,
    help="dropout rate for first 2 dense layers",
    default=0.6,
    type=float
)
ap.add_argument(
    "-i",
    "--extra-conv2d-count",
    required=False,
    help="Number of extra conv2d layers to add that do not change the size of the image",
    default=1,
    type=int
)



args = vars(ap.parse_args())
print(f"\n{args=}\n")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import tensorflow as tf
import tensorflow.data as data
import tensorflow.keras as keras
import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.activations as activations

print(f"\n\nTensorflow version: {tf.__version__}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
class Model:
    def __init__(self, input_size, dropout_rate, l1, l2, extra_conv2d_count):
        # Input: 387 x 387 x 3

        regularizer = keras.regularizers.l1_l2(l1=l1, l2=l2)

        self.model = tf.keras.Sequential()

        for i in range(extra_conv2d_count):
            if i == 0:
                self.model.add(layers.Conv2D(
                    filters = 10 + i,
                    kernel_size = 3,
                    strides = 1,
                    activation = activations.relu,
                    kernel_regularizer = regularizer,
                    input_shape = input_size,
                    padding = "same",
                ))
            else:
                self.model.add(layers.Conv2D(
                    filters = 10 + i,
                    kernel_size = 3,
                    strides = 1,
                    activation = activations.relu,
                    kernel_regularizer = regularizer,
                    padding = "same",
                ))

            self.model.add(layers.BatchNormalization())

        if extra_conv2d_count > 0:
            self.model.add(layers.Conv2D(
                filters = 15 + extra_conv2d_count,
                kernel_size = 15,
                strides = 8,
                activation = activations.relu,
                kernel_regularizer = regularizer,
            ))
        else:
            self.model.add(layers.Conv2D(
                filters = 15 + extra_conv2d_count,
                kernel_size = 15,
                strides = 8,
                activation = activations.relu,
                kernel_regularizer = regularizer,
                input_shape = input_size,
            ))
        # Size: 47 x 47 x 15

        self.model.add(layers.BatchNormalization())

        self.model.add(layers.MaxPool2D(
            pool_size = 3,
            strides = 2,
        ))
        # Size: 23 x 23 x 15

        self.model.add(layers.Conv2D(
            filters = 20 + extra_conv2d_count,
            kernel_size = 3,
            strides = 1,
            activation = activations.relu,
            kernel_regularizer = regularizer,
        ))
        # Size: 21 x 21 x 20

        self.model.add(layers.BatchNormalization())

        self.model.add(layers.MaxPool2D(
            pool_size = 3,
            strides = 2,
        ))
        # Size: 10 x 10 x 20

        self.model.add(layers.Flatten())
        # Size: 2000

        self.model.add(layers.Dense(units = 256, activation = activations.relu,    kernel_regularizer = regularizer))
        self.model.add(layers.Dropout(rate = dropout_rate))
        self.model.add(layers.Dense(units = 64,  activation = activations.relu,    kernel_regularizer = regularizer))
        self.model.add(layers.Dropout(rate = dropout_rate))
        self.model.add(layers.Dense(units = 16,  activation = activations.relu,    kernel_regularizer = regularizer))
        self.model.add(layers.Dense(units = 5,   activation = activations.softmax, kernel_regularizer = regularizer,))

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def set_loss(self, loss):
        self.loss = loss

    def set_metrics(self, metrics):
        self.metrics = metrics

    def compile(self):
        self.model.compile(
            optimizer = self.optimizer,
            loss = self.loss,
            metrics = self.metrics
        )

    def summary(self):
        self.model.summary()

    def load_weights(self, path):
        self.model.load_weights(path)

    def save(self, path):
        self.model.save(path)
# ---------------------------------------------------------------------------- #
       

# ---------------------------------------------------------------------------- #
print("\nLoading data...")

LEARN_DATA_FOLDER = "dataset/learn"
VALID_DATA_FOLDER = "dataset/valid"
DATA_SHAPE = (387, 387)

# NOTE: will be split into 47 batches

# TODO: data augmentation: random_crop, random_brightness, random_contrast

train = utils.image_dataset_from_directory(
    LEARN_DATA_FOLDER,
    label_mode='categorical',
    image_size=DATA_SHAPE
)
print(f"{train.class_names=}")
train = train.cache().prefetch(buffer_size = data.AUTOTUNE)

valid = utils.image_dataset_from_directory(
    VALID_DATA_FOLDER,
    label_mode='categorical',
    image_size=DATA_SHAPE
)
print(f"{valid.class_names=}")
valid = valid.cache().prefetch(buffer_size = data.AUTOTUNE)

print(f"{train=}")
print(f"{valid=}")
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
model = Model(
    input_size=(DATA_SHAPE[0], DATA_SHAPE[1], 3),
    dropout_rate=args["dropout"],
    extra_conv2d_count=args["extra_conv2d_count"],
    l1=args["l1"],
    l2=args["l2"],
)

lr_schedule = keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate = args["learning_rate"],
    decay_steps = args["decay_steps"],
    decay_rate = args["decay_rate"],
)

model.set_optimizer(optimizers.Adam(learning_rate = lr_schedule))
model.set_loss(losses.CategoricalCrossentropy())
model.set_metrics([
    'accuracy',
    tf.keras.metrics.TopKCategoricalAccuracy(k=args["top_k_categorical_accuracy"])
])
model.compile()

model.summary()

if args["load_checkpoint_path"] is not None:
    model.load_weights(args["load_checkpoint_path"])
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
print("\nTraining model...")

callbacks = []

if args["checkpoint_save_path"] is not None:
    if args["frequency_checkpoint"] == 1:
        save_freq = 'epoch'
    else:
        num_batches = len(train)
        save_freq = args["frequency_checkpoint"] * num_batches

    save_callback = keras.callbacks.ModelCheckpoint(
        filepath = args["checkpoint_save_path"],
        monitor = "val_accuracy",
        verbose = 1,
        save_weights_only = True,
        save_freq = save_freq,
    )
    callbacks.append(save_callback)

if args["plot_history_save_path"] is not None:
    plot_callback = keras.callbacks.CSVLogger(args["plot_history_save_path"], append=True)
    callbacks.append(plot_callback)

try:
    history = model.model.fit(
        train,
        epochs = args["epochs"],
        verbose = 1,
        callbacks = callbacks,
        validation_data = valid,
    )

    print(f"Training finished.")
except KeyboardInterrupt: pass

if args["save_path"] is not None:
    print(f"Saving model to {args['save_path']}")
    model.save(args["save_path"])
# ---------------------------------------------------------------------------- #
