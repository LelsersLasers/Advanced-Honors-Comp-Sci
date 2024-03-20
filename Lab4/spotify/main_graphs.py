import graphs.heat_map
import graphs.time_line
import graphs.genre_bar


# ---------------------------------------------------------------------------- #
import argparse

ap = argparse.ArgumentParser()


ap.add_argument(
    "-c",
    "--correlation",
    required=False,
    help="display heat map of correlation between categories",
	action="store_false",
)
ap.add_argument(
	"-t",
	"--time-line",
	required=False,
	help="display line graph of average category over time",
	action="store_false",
)
ap.add_argument(
	"-g",
	"--genre-bar",
	required=False,
	help="display bar graph of average category per genre",
	action="store_false",
)
ap.add_argument(
	"-m",
	"--method",
	required=False,
	help="method for correlation calculation",
	choices=["pearson", "kendall", "spearman"],
	default="pearson"
)
ap.add_argument(
	"-v",
	"--categories-values",
	required=False,
	help="categories to display",
	nargs="+",
	default=["acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence", "popularity"]
)


args = vars(ap.parse_args())
print(f"\n{args=}\n")
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
for arg, value in args.items():
	if value:
		if arg == "correlation":
			graphs.heat_map.full_heat_map(args["categories_values"], args["method"])
		elif arg == "time_line":
			graphs.time_line.time_line_full(args["categories_values"])
		elif arg == "genre_bar":
			graphs.genre_bar.genre_bar_full(args["categories_values"])