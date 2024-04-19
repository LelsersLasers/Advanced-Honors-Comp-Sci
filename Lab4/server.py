import flask

import graphs.heat_map
import graphs.time_line
import graphs.group_bar

app = flask.Flask(__name__)


def create_response(value):
    response = flask.jsonify(value)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Origin, Content-Type, X-Auth-Token")
    return response

@app.route("/all_graphs", methods=["GET"])
def all_graphs():
    categories_values = []
    for arg, value in flask.request.args.items():
        if value == "true":
            categories_values.append(arg)

    id = flask.request.args.get("id")
    correlation_method = flask.request.args.get("correlation_method")


    heat_map = graphs.heat_map.full_heat_map(categories_values, correlation_method, id)
    time_line = graphs.time_line.time_line_full(categories_values, id)
    genre_bar = graphs.group_bar.bar_full(categories_values, "genres", id)
    artists = graphs.group_bar.bar_full(categories_values, "artists", id)

    response_dict = {
        "heat_map": heat_map,
        "time_line": time_line,
        "genre_bar": genre_bar,
        "artists": artists,
    }
    return create_response(response_dict)

app.run(debug=False, port=5000, host="0.0.0.0", threaded=False, processes=1)