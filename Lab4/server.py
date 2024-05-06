import flask
import flask_cors

import urllib.parse

import graphs.heat_map
import graphs.time_line
import graphs.group_bar

import styles.simple
import styles.predictor
import styles.autoencoder
import styles.cnn

import distances

# import spotify
# import json
import data

app = flask.Flask(__name__)


def create_response(value):
    response = flask.jsonify(value)
    # flask_cors.cross_origin() does this process better
    # response.headers.add("Access-Control-Allow-Origin", "*")
    # response.headers.add("Access-Control-Allow-Methods", "GET, POST")
    # response.headers.add("Access-Control-Allow-Headers", "Origin, Content-Type, X-Auth-Token")
    return response

@app.route("/graphs_bs64/<graph>", methods=["GET"])
@flask_cors.cross_origin()
def graphs_bs64(graph):
    categories_values = []
    for arg, value in flask.request.args.items():
        if value == "true":
            categories_values.append(arg)

    id = flask.request.args.get("id")
    correlation_method = flask.request.args.get("correlation_method")

    if graph == "heat_map":
        output = graphs.heat_map.full_heat_map(categories_values, correlation_method, id)
    elif graph == "time_line":
        output = graphs.time_line.time_line_full(categories_values, id)
    elif graph == "genre_bar":
        output = graphs.group_bar.bar_full(categories_values, "genres", id)
    elif graph == "artists":
        output = graphs.group_bar.bar_full(categories_values, "artists", id)

    response_dict = {
        "graph": output
    }
    return create_response(response_dict)

# @app.route("/spotify/token", methods=["GET"])
# def get_token():
#     # read json from .cache
#     with open(".cache", "r") as file:
#         data = json.load(file)
#     return create_response(data)

# @app.route("/spotify/search/<q>", methods=["GET"])
# def search_spotify(q):
#     print(f"Searching for: {q}")
#     result = spotify.search_spotify(sp, q)
#     print(f"Found {len(result)} results")
#     return create_response(result)

@app.route("/spotify/search/<q>", methods=["GET"])
@flask_cors.cross_origin()
def search_spotify(q):
    title = urllib.parse.unquote(q)
    print(f"Searching: {title}")
    results = data.search_song(title)
    print(f"Best match: {results[0]}")
    return create_response(results)

@app.route("/spotify/fetch/<id>", methods=["GET"])
@flask_cors.cross_origin()
def fetch_spotify(id):
    print(f"Fetching: {id}")
    result = data.fetch_song(id)
    print(f"{id} {result}")
    return create_response(result)

@app.route("/recommendations", methods=["POST"])
@flask_cors.cross_origin()
# def recommendations(model, dist, index, google_mode):
def recommendations():
    print(flask.request.json)
    model = flask.request.json.get("model")
    dist = flask.request.json.get("dist")

    index = flask.request.json.get("index")
    index = int(index)

    google_mode = flask.request.json.get("google_mode")
    google_mode = google_mode == "true"
    
    
    print(f"Getting recommendations for: {index} using {model} and {dist}")

    model_dict = {
        "simple":      styles.simple,
        "predictor":   styles.predictor,
        "autoencoder": styles.autoencoder,
        "cnn":         styles.cnn
    }
    dist_dict = {
        "cos": distances.cos_dist,
        "mae": distances.mae_dist,
        "mse": distances.mse_dist,
        "euclidean": distances.euclidean_dist,
        "dot": distances.dot_product
    }

    if model == "cnn":
        if index > 0:
            results = (model_dict[model]).predict(google_mode, index, dist_dict[dist], False)
        else:
            image_b64 = flask.request.form.get("image_b64")
            print(f"Image b64: {image_b64}")
            # results = (model_dict[model]).predict(google_mode, image_b64, dist_dict[dist], False)
    else:
        results = (model_dict[model]).predict(index, dist_dict[dist], False)
    return create_response(results)


app.run(debug=False, port=5000, host="0.0.0.0", threaded=False, processes=1)