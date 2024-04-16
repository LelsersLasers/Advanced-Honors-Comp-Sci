<script>


</script>


<div id="holder">
	<div id="left">
		<h1>Graphs</h1>

		<h3>Categories</h3>

		<input type="checkbox" name="year_checkbox" checked="checked" />
		<label for="year_checkbox">Year</label>
		<br />

		<input type="checkbox" name="popularity_checkbox" checked="checked" />
		<label for="popularity_checkbox">Popularity</label>
		<br />

		<input type="checkbox" name="acousticness_checkbox" checked="checked" />
		<label for="acousticness_checkbox">Acousticness</label>
		<br />

		<input type="checkbox" name="danceability_checkbox" checked="checked" />
		<label for="danceability_checkbox">Danceability</label>
		<br />

		<input type="checkbox" name="duration_ms_checkbox" checked="checked" />
		<label for="duration_ms_checkbox">Duration (ms)</label>
		<br />

		<input type="checkbox" name="energy_checkbox" checked="checked" />
		<label for="energy_checkbox">Energy</label>
		<br />

		<input type="checkbox" name="instrumentalness_checkbox" checked="checked" />
		<label for="instrumentalness_checkbox">Instrumentalness</label>
		<br />

		<input type="checkbox" name="liveness_checkbox" checked="checked" />
		<label for="liveness_checkbox">Liveness</label>
		<br />

		<input type="checkbox" name="loudness_checkbox" checked="checked" />
		<label for="loudness_checkbox">Loudness</label>
		<br />

		<input type="checkbox" name="speechiness_checkbox" checked="checked" />
		<label for="speechiness_checkbox">Speechiness</label>
		<br />

		<input type="checkbox" name="tempo_checkbox" checked="checked" />
		<label for="tempo_checkbox">Tempo</label>
		<br />

		<input type="checkbox" name="valence_checkbox" checked="checked" />
		<label for="valence_checkbox">Valence</label>
		<br />

		<br />



		<h2>Correlation</h2>

		<input type="checkbox" name="correlation_checkbox" checked="checked" />
		<label for="correlation_checkbox">Active</label>
		<br />

		<label for="correlation_method">Correlation Method:</label>
		<select name="correlation_method">
			<option value="pearson">Pearson</option>
			<option value="spearman">Spearman</option>
			<option value="kendall">Kendall</option>
		</select>

		<br />


		<h2>Timeline</h2>

		<input type="checkbox" name="timeline_checkbox" checked="checked" />
		<label for="timeline_checkbox">Active</label>

		<br />


		<h2>Genre Bar</h2>

		<input type="checkbox" name="genre_bar_checkbox" checked="checked" />
		<label for="genre_bar_checkbox">Active</label>

		<br />


		<h2>Artists</h2>

		<input type="checkbox" name="artists_checkbox" checked="checked" />
		<label for="artists_checkbox">Active</label>

		<br />


		<br />

		<a href="/">
			<button>Back to Home</button>
		</a>

	</div>
	<div id="right">
		
	</div>
</div>


<style>
	#holder {
		display: flex;
	}

	#left {
		width: 33%;
	}

	#right {
		width: 66%;
	}
</style>