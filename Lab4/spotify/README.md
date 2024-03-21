# Spotify or something

## Data

- DATASET: https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset
- BASE: https://www.kaggle.com/code/vatsalmavani/music-recommendation-system-using-spotify-dataset/input
- Using: `data.csv`

## Data Preprocessing

- Don't need: artists, explicit, id, mode, name
- Build similarity based on popularity for predictor style

## Helpful

- Read CSV: https://www.tensorflow.org/tutorials/load_data/csv
- Tensorflow Similarity:
	- https://github.com/tensorflow/similarity/blob/master/examples/supervised_hello_world.ipynb
	- https://blog.tensorflow.org/2021/09/introducing-tensorflow-similarity.html
- Google Similarity overview:
    - https://developers.google.com/machine-learning/clustering/similarity/supervised-similarity
- ChatGPT: https://chat.openai.com/share/d170d9be-4828-4f9f-a6cb-6e378c113590
- spotipy: https://spotipy.readthedocs.io/en/2.22.1/
- Correlation: 
    - Auto: https://www.tensorflow.org/probability/api_docs/python/tfp/stats/auto_correlation
    - Pearson: https://www.tensorflow.org/probability/api_docs/python/tfp/stats/correlation

## Ideas

- Graphs:
    - Correlation between categories
        - Input: (method)
        - Output: (heat map)
    - Average category over time
        - Input: (categories)
        - Output: (line graph)
    - Average category per genre
        - Input: (categories)
        - Output: (group bar graph)
    - Average category per artist
        - Input: (categories)
        - Output: (group bar graph)
- Similarities:
    - Base:
        - Distance between 13 input features
    - Predictor style:
        - Distance between embeddings layer of a DNN with:
            - Input: 12 features (all but popularity)
            - Hidden layers (Normalization, Dense, Dropout)
            - Output: 1 feature (popularity)
    - Autoencoder style:
        - Distance between embeddings layer of a DNN with:
            - Input: 13 features
            - Hidden layers (Normalization, Dense, Dropout)
            - Output: 13 features
    - Image:
        - Distance between embeddings layer of a CNN with:
            - Input: image
            - Hidden layers (Conv2D, BatchNormalization, MaxPooling2D, Flatten, Dense, Dropout)
            - Output: 13 features
- Similarity inputs:
    - Song: use `data.csv`
    - Artist: use `data.csv`
    - Playlist:
        - For every song in playlist, use `data.csv` (filter out duplicates, etc)
        - Train a DNN on just the playlist?
    - Image: use `data.csv` songs + use `spotipy` to get album cover art
        - Can still use a random image as input to get songs that match the image!

## COME BACK TOO

- predictor:
    - argparse/inputs: epochs, activations, learning rate, optimizer, loss
- multiprocessing pool map
    - how does it play with the alive bar?