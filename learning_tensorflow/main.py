import tensorflow as tf
import tensorflow.keras.utils as utils


import time
seed = time.time_ns() & 0xfffffff

DATA_SET_FOLDER = "defungi"
print(f"Tensorflow version: {tf.__version__}")


train, validation = utils.image_dataset_from_directory(
    DATA_SET_FOLDER,
    label_mode='categorical',
    image_size=(224, 224),
    seed=seed,
    validation_split=0.3,
    subset='both',
)

print(train, validation)
