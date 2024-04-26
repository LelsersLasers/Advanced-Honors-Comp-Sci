import flask

import graphs.heat_map
import graphs.time_line
import graphs.group_bar

import spotify

app = flask.Flask(__name__)

sp = spotify.create_sp()


def create_response(value):
    response = flask.jsonify(value)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Origin, Content-Type, X-Auth-Token")
    return response

@app.route("/graphs_bs64/<graph>", methods=["GET"])
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

@app.route("/spotify/search/<q>", methods=["GET"])
def search_spotify(q):
    print(f"Searching for: {q}")
    result = spotify.search_spotify(sp, q)
    print(f"Found {len(result)} results")
    return create_response(result)

@app.route("/spotify/fetch/<id>", methods=["GET"])
def fetch_spotify(id):
    print(f"Fetching: {id}")
    result = spotify.fetch_track(sp, id)
    print(f"Found {result}")
    return create_response(result)

app.run(debug=False, port=5000, host="0.0.0.0", threaded=False, processes=1)