import time
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.applications.resnet50 as resnet50

print("\n\nStarting programing...\n")
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
    # classifier_activation="softmax"
)

resnet.trainable = False

inputs = keras.Input(shape=(224, 224, 3))
outputs = resnet(inputs)
outputs = layers.Dense(5, activation="softmax")(outputs)

optimizer = optimizers.legacy.Adam(learning_rate = 0.00001)
loss = losses.CategoricalCrossentropy()

model = keras.Model(inputs, outputs)
model.compile(
    optimizer = optimizer,
    loss = loss,
    metrics = ['accuracy']
)

print(f"{resnet=}")
print(f"{inputs=}")
print(f"{outputs=}")
print(f"{optimizer=}")
print(f"{loss=}")
print(f"{model=}")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
print("\nTraining model")
model.fit(
    train,
    batch_size = 32,
    epochs = 10,
    verbose = 1,
    validation_batch_size = 32
)
