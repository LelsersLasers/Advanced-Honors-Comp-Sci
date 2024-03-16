
import data


# ---------------------------------------------------------------------------- #
import tensorflow as tf
# import tensorflow.data as data
# import tensorflow.keras as keras
# import tensorflow.keras.utils as utils
import tensorflow.keras.layers as layers
# import tensorflow.keras.losses as losses
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.activations as activations

import tensorflow_similarity as tfsim
import tensorflow_similarity.losses as tfsim_losses
import tensorflow_similarity.samplers as tfsim_samplers

print(f"\n\nTensorflow version: {tf.__version__}")
print(f"TensorFlow Similarity version {tfsim.__version__}\n\n")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
data_features, data_labels = data.load_data()
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def make_model():
	normalize = layers.Normalization()
	normalize.adapt(data_features)

	inputs = layers.Input(shape=(data_features.shape[1],))
	x = normalize(inputs)
	x = layers.Dense(100, activation=activations.relu)(x)
	x = layers.Dense(100, activation=activations.relu)(x)
	x = layers.Dense(100, activation=activations.relu)(x)
	outputs = tfsim.layers.MetricEmbedding(64)(x)

	model = tfsim.models.SimilarityModel(inputs, outputs)
	return model

model = make_model()

optimizer = optimizers.Adam(learning_rate = 0.001)
loss = tfsim_losses.MultiSimilarityLoss(distance='cosine')

model.compile(
	optimizer=optimizer,
	loss=loss,
)

print(model.summary())
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
CLASSES = list(set(data_labels))

sampler = tfsim.samplers.MultiShotMemorySampler(
	data_features,
	data_labels,
	class_list=CLASSES,
	classes_per_batch=len(CLASSES),
	steps_per_epoch=5000,
)

model.fit(
	sampler,
	epochs=5,
)


x_index, y_index = tfsim_samplers.select_examples(data_features, data_labels, CLASSES, 200)
model.reset_index()
model.index(x_index, y_index, data=x_index)

model.save('output/try1-fullsave')
# ---------------------------------------------------------------------------- #


