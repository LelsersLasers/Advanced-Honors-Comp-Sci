EMBEDDINGS_PATH = 'output/embeddings.csv'
TEST_INDEX = 18032 - 2


# ---------------------------------------------------------------------------- #
import alive_progress
import numpy as np
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
import json

def load_embeddings():
    all_embeddings = []
    with open(EMBEDDINGS_PATH, 'r') as file:
        file.readline() # skip header
        for line in file:
            song_str, embedding_str = line.split('^^')
            song = json.loads(song_str.strip())
            embedding = np.array(json.loads(embedding_str.strip()))
            all_embeddings.append((song, embedding))
    return all_embeddings


all_embeddings = load_embeddings()
base_embedding = all_embeddings[TEST_INDEX]
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def cosine_distance(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


print("Calculating distances...")
coses = []
song_count = len(all_embeddings)
with alive_progress.alive_bar(song_count) as bar:
    for embedding in all_embeddings:
        a = base_embedding[1]
        song, b = embedding
        cos = cosine_distance(a, b)
        coses.append((song, cos))
        bar()
coses.sort(key=lambda x: x[1], reverse=True)
print("Sorted by cosine distance")
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
def clamp(x, a, b):
    return max(a, min(b, x))

print("Top 10 most similar songs:")
print("BASE SONG:", base_embedding[0]['name'], "by", base_embedding[0]['artists'])
for i in range(10):
    song, cos = coses[i]
    cos = clamp(cos, -1, 1)
    angle = np.arccos(cos) * 180 / np.pi
    artists_str = ', '.join(song['artists'])
    print(f"{i + 1}) {song['name']} by {song['artists']} (cos: {cos:.3f}, ({angle:.2f}°)")
# ---------------------------------------------------------------------------- #