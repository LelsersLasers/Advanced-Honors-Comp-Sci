import tensorflow as tf
import tensorflow.keras.layers as layers
import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.activations as activations

print(f"\n\nTensorflow version: {tf.__version__}")


# import tensorflow.keras as keras
# import tensorflow.keras.utils as utils
# import tensorflow.keras.layers as layers
# import tensorflow.keras.losses as losses
# import tensorflow.keras.optimizers as optimizers

# Skip getting the data

class Model:
    def __init__(self, input_size):
        # Input: 387 x 387 x 3

        self.model = tf.keras.Sequential()

        self.model.add(layers.Conv2D(
            filters = 10,
            kernel_size = 19,
            strides = 8,
            activation = activations.relu,
            input_shape = input_size,
        ))
        # Size: 47 x 47 x 10

        self.model.add(layers.MaxPool2D(
            pool_size = 3,
            strides = 2,
        ))
        # Size: 23 x 23 x 10

        self.model.add(layers.Conv2D(
            filters = 14,
            kernel_size = 3,
            strides = 1,
            activation = activations.relu,
        ))
        # Size: 21 x 21 x 14

        self.model.add(layers.MaxPool2D(
            pool_size = 3,
            strides = 2,
        ))
        # Size: 10 x 10 x 14

        self.model.add(layers.Flatten())
        # Size: 1400

        self.model.add(layers.Dense(units = 256, activation = activations.relu))
        self.model.add(layers.Dense(units = 64,  activation = activations.relu))
        self.model.add(layers.Dense(units = 16,  activation = activations.relu))
        self.model.add(layers.Dense(units = 5,   activation = activations.softmax))

        self.optimizer = optimizers.Adam(learning_rate = 0.0001)
        self.loss = losses.CategoricalCrossentropy()

        self.model.compile(
            optimizer = self.optimizer,
            loss = self.loss,
            metrics = [ 'accuracy' ]
        )



# model = Model(input_size=(387, 387, 3))
model.summary()
