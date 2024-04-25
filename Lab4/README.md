# Song Recommender

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
- spotipy:
    - https://spotipy.readthedocs.io/en/2.22.1/
    - https://developer.spotify.com/documentation/web-api/reference/get-several-tracks
- Correlation: 
    - Auto: https://www.tensorflow.org/probability/api_docs/python/tfp/stats/auto_correlation
    - Pearson: https://www.tensorflow.org/probability/api_docs/python/tfp/stats/correlation
- shadcn-svelte: https://www.shadcn-svelte.com/
- https://docs.opencv.org/4.x/d1/db7/tutorial_py_histogram_begins.html
- Non-sequential model: https://stackoverflow.com/questions/49618986/neural-network-in-keras-with-two-different-input-types-images-and-values

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
    - Song (text, direct id): use `data.csv`
    - **Artist (text, direct id): use `data_by_artist.csv`**
    - Playlist (direct id):
        - For every song in playlist, use `data.csv` (filter out duplicates, etc)
        - Do average embedding for songs in playlist + closest song to each individual song
    - Image (text search, file path): use `data.csv` songs + use `spotipy` to get album cover art
        - Can still use a random image as input to get songs that match the image!

## Run

```
main graphs <args...>
main [predictor, autoencoder, cnn] [train, embeddings] <args...>
main [predictor, autoencoder, cnn, simple] predict [search, id] (input)
TODO: image input!
```

## COME BACK TOO

- predictor:
    - argparse/inputs: epochs, activation, learning rate, optimizer, loss
- embeddings:
    - How many layers from the end to use
- multiprocessing pool map
    - how does it play with the alive bar?