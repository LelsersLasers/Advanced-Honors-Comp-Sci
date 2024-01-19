import tensorflow as tf
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.activations as activations

print(f"\n\nTensorflow version: {tf.__version__}")

inputs = tf.keras.Input(shape=(387, 387, 3))

outputs = layers.Conv2D(
    filters = 10,
    kernel_size = 19,
    strides = 8,
    activation = activations.relu,
)(inputs)
outputs = layers.MaxPool2D(
    pool_size = 3,
    strides = 2,
)(outputs)
outputs = layers.Conv2D(
    filters = 14,
    kernel_size = 3,
    strides = 1,
    activation = activations.relu,
)(outputs)
outputs = layers.MaxPool2D(
    pool_size = 3,
    strides = 2,
)(outputs)
outputs = layers.Flatten()(outputs)
outputs = layers.Dense(units = 256, activation = activations.relu)(outputs)
outputs = layers.Dense(units = 64,  activation = activations.relu)(outputs)
outputs = layers.Dense(units = 16,  activation = activations.relu)(outputs)
outputs = layers.Dense(units = 5,   activation = activations.softmax)(outputs)

model = tf.keras.Model(inputs=inputs, outputs=outputs)

optimizer = optimizers.Adam(learning_rate = 0.0001)
loss = losses.CategoricalCrossentropy()

model.compile(
    optimizer = optimizer,
    loss = loss,
    metrics = [ 'accuracy' ]
)



model.summary()
