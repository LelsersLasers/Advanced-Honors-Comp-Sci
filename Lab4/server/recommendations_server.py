import flask
import flask_cors

import cv2
import numpy as np
import base64

import styles.simple
import styles.predictor
import styles.autoencoder
import styles.expansion
import styles.cnn

import distances
import data

PORT = 5000


def thread():
    app = flask.Flask(__name__)

    def create_response(value):
        response = flask.jsonify(value)
        # flask_cors.cross_origin() does this process better
        # response.headers.add("Access-Control-Allow-Origin", "*")
        # response.headers.add("Access-Control-Allow-Methods", "GET, POST")
        # response.headers.add("Access-Control-Allow-Headers", "Origin, Content-Type, X-Auth-Token")
        return response


    @app.route("/spotify/search", methods=["POST"])
    @flask_cors.cross_origin()
    def search_spotify():
        title = flask.request.json.get("title", "")
        artist = flask.request.json.get("artist", "")

        print(f"Searching: {title} by {artist}")
        results = data.search_song(title, artist)
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
    def recommendations():
        model = flask.request.json.get("model")
        dist = flask.request.json.get("dist")

        index = flask.request.json.get("index")
        index = int(index)

        google_mode = flask.request.json.get("google_mode")

        print("GOOGLE MODE:", google_mode)
        
        
        print(f"Getting recommendations for: {index} using {model} and {dist}")

        model_dict = {
            "simple":      styles.simple,
            "predictor":   styles.predictor,
            "autoencoder": styles.autoencoder,
            "expansion":   styles.expansion,
            "cnn":         styles.cnn
        }
        dist_dict = {
            "cos":       distances.cos_dist,
            "mae":       distances.mae_dist,
            "euclidean": distances.euclidean_dist,
            "dot":       distances.dot_product
        }

        if model == "cnn":
            if index > 0:
                results = (model_dict[model]).predict(google_mode, index=index, dist=dist_dict[dist], display=False)
            else:
                input_b64 = flask.request.json.get("input_b64")
                print(f"Received image: {input_b64[:50]}...")
                
                nparr = np.fromstring(base64.b64decode(input_b64), np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                image = cv2.resize(image, (128, 128))

                print(f"Image shape: {image.shape}")

                intermediate_model = (model_dict[model]).create_intermediate_model(google_mode)

                nn_input = np.expand_dims(image, axis=0)
                embedding = intermediate_model(nn_input)
                embedding = np.squeeze(embedding.numpy(), axis=0)

                results = (model_dict[model]).predict(google_mode, embedding=embedding, dist=dist_dict[dist], display=False)
        elif model == "simple":
            extra_categories_to_remove = flask.request.json.get("extra_categories_to_remove")
            print(f"Removing: {extra_categories_to_remove}")
            results = (model_dict[model]).predict(index=index, dist=dist_dict[dist], display=False, extra_categories_to_remove=extra_categories_to_remove)
        else:
            results = (model_dict[model]).predict(index=index, dist=dist_dict[dist], display=False)
        return create_response(results)


    app.run(debug=False, port=PORT, host="0.0.0.0", processes=5, threaded=False)