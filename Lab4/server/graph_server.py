import flask
import flask_cors
import graphs.heat_map
import graphs.time_line
import graphs.group_bar

PORT = 5001


def thread():
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
    
    app.run(debug=False, port=PORT, host="0.0.0.0", threaded=False, processes=1)