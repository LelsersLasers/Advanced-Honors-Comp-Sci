import tensorflow as tf
import tensorflow.keras.utils as utils
import tensorflow.keras.applications.resnet50 as resnet50

import time

print("\n\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n")
print(f"Tensorflow version: {tf.__version__}")


# ---------------------------------------------------------------------------- #
print("\nLoading data...")
seed = time.time_ns() & 0xfffffff

DATA_SET_FOLDER = "defungi"

train, validation = utils.image_dataset_from_directory(
    DATA_SET_FOLDER,
    label_mode='categorical',
    image_size=(224, 224),
    seed=seed,
    validation_split=0.3,
    subset='both',
)

train = train.map(lambda x, y: (resnet50.preprocess_input(x), y))
validation = validation.map(lambda x, y: (resnet50.preprocess_input(x), y))

print(f"{train=}")
print(f"{validation=}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
print("\nCreating model")
resnet = resnet50.ResNet50(
    include_top=True,
    weights='imagenet',
    classifier_activation="softmax"
)

print(f"{resnet=}")
# ---------------------------------------------------------------------------- #
