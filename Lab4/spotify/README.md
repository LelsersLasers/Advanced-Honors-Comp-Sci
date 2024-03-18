# Spotify or something

## Data

- DATASET: https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset
- BASE: https://www.kaggle.com/code/vatsalmavani/music-recommendation-system-using-spotify-dataset/input
- Using: `data.csv`

## Data Preprocessing

- Don't need: artists, explicit, id, mode, name
- Build similarity based on popularity

## Helpful

- Read CSV: https://www.tensorflow.org/tutorials/load_data/csv
- Tensorflow Similarity:
	- https://github.com/tensorflow/similarity/blob/master/examples/supervised_hello_world.ipynb
	- https://blog.tensorflow.org/2021/09/introducing-tensorflow-similarity.html
- Google Similarity overview:
    - https://developers.google.com/machine-learning/clustering/similarity/supervised-similarity
- ChatGPT: https://chat.openai.com/share/d170d9be-4828-4f9f-a6cb-6e378c113590

## Ideas

- Similarity between songs
    - Built from data.csv
    - If given a song, recommend similar songs
- Similarity between artists
    - Built from data.csv
    - If given an artist, recommend similar artists
- Recommend by playlist?
    - Given a playlist, recommend songs
    - Use either/both generate from:
        - The similarity built from data.csv
        - Built a new similarity based on just the playlist
- Correlation between features
    - Ex: popularity vs danceability

## Copied ideas

- Correlation: https://www.tensorflow.org/probability/api_docs/python/tfp/stats/auto_correlation
- Average/median x category over time
- Average/median x category per genre