import argparse

ap = argparse.ArgumentParser()

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
    "-s",
    "--save-path",
    required=False,
    help="location to save model after training",
    default=None,
)

args = vars(ap.parse_args())
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.models as models
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.applications as applications
import tensorflow.keras.applications.mobilenet_v3 as mobilenet_v3

print(f"\n\nTensorflow version: {tf.__version__}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
print("\nLoading data...")

DATA_SET_FOLDER = "learn-dataset"

train = utils.image_dataset_from_directory(
    DATA_SET_FOLDER,
    label_mode='categorical',
    image_size=(224, 224),
)

train = train.map(lambda x, y: (mobilenet_v3.preprocess_input(x), y))

print(f"{train=}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
print("\nCreating model...")

mobilenet = applications.MobileNetV3Large(
    include_top=True,
    weights='imagenet',
    # classifier_activation="softmax"
)

mobilenet.trainable = False

inputs = keras.Input(shape=(224, 224, 3))
outputs = mobilenet(inputs)
outputs = layers.Dense(5, activation="softmax")(outputs)

# Transfer learning: use lower learning_rate
optimizer = optimizers.legacy.Adam(learning_rate = 0.00001)
loss = losses.CategoricalCrossentropy()

model = keras.Model(inputs, outputs)
model.compile(
    optimizer = optimizer,
    loss = loss,
    metrics = ['accuracy']
)

if args["load_checkpoint_path"] is not None:
    model.load_weights(args["load_checkpoint_path"])

print(f"{mobilenet=}")
print(f"{inputs=}")
print(f"{outputs=}")
print(f"{optimizer=}")
print(f"{loss=}")
print(f"{model=}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
print("\nTraining model...")

if args["checkpoint_save_path"] is not None:

    save_callback = keras.callbacks.ModelCheckpoint(
        filepath = args["checkpoint_save_path"],
        monitor = "val_accuracy",
        verbose = 1,
        save_weights_only = True,
    )
    callbacks = [save_callback]
else:
    callbacks = []

model.fit(
    train,
    batch_size = 32,
    epochs = 2,
    verbose = 1,
	callbacks = callbacks,
)

print(f"Training finished.")

if args["save_path"] is not None:
    print(f"Saving model to {args['save_path']}")
    model.save(args["save_path"])
# ---------------------------------------------------------------------------- #