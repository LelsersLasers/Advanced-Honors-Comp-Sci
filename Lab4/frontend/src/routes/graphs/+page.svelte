<script>
	import { getContext } from 'svelte';
	const FLASK_URL = getContext('flask_url');

	let checked_values = {
		year: true,
		popularity: true,
		acousticness: true,
		danceability: true,
		duration_ms: true,
		energy: true,
		instrumentalness: true,
		liveness: true,
		loudness: true,
		speechiness: true,
		tempo: true,
		valence: true,
		correlation_active: true,
		correlation_method: "pearson",
		timeline_active: true,
		genre_bar_active: true,
		artists_active: true
	};
	function updated_checked_values() {
		checked_values.year = document.querySelector('input[name="year_checkbox"]').checked;
		checked_values.popularity = document.querySelector('input[name="popularity_checkbox"]').checked;
		checked_values.acousticness = document.querySelector('input[name="acousticness_checkbox"]').checked;
		checked_values.danceability = document.querySelector('input[name="danceability_checkbox"]').checked;
		checked_values.duration_ms = document.querySelector('input[name="duration_ms_checkbox"]').checked;
		checked_values.energy = document.querySelector('input[name="energy_checkbox"]').checked;
		checked_values.instrumentalness = document.querySelector('input[name="instrumentalness_checkbox"]').checked;
		checked_values.liveness = document.querySelector('input[name="liveness_checkbox"]').checked;
		checked_values.loudness = document.querySelector('input[name="loudness_checkbox"]').checked;
		checked_values.speechiness = document.querySelector('input[name="speechiness_checkbox"]').checked;
		checked_values.tempo = document.querySelector('input[name="tempo_checkbox"]').checked;
		checked_values.valence = document.querySelector('input[name="valence_checkbox"]').checked;
		checked_values.correlation_active = document.querySelector('input[name="correlation_active"]').checked;
		checked_values.correlation_method = document.querySelector('select[name="correlation_method"]').value;
		checked_values.timeline_active = document.querySelector('input[name="timeline_active"]').checked;
		checked_values.genre_bar_active = document.querySelector('input[name="genre_bar_active"]').checked;
		checked_values.artists_active = document.querySelector('input[name="artists_active"]').checked;
	}

	$: {
		console.log(checked_values);
		fetch(FLASK_URL + "/graphs", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(checked_values)
		})
			.then(response => response.json())
			.then(data => {
				console.log(data);
				for (let key in data) {
					console.log(key);
					console.log(data[key]);
				}
				// document.getElementById('right').innerHTML = data.html;
			})
			.catch((error) => {
				console.error('Error:', error);
			});
	}

</script>


<div id="holder">
	<div id="left">
		<h1>Graphs</h1>

		<h3>Categories</h3>

		<input type="checkbox" name="year_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="year_checkbox">Year</label>
		<br />

		<input type="checkbox" name="popularity_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="popularity_checkbox">Popularity</label>
		<br />

		<input type="checkbox" name="acousticness_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="acousticness_checkbox">Acousticness</label>
		<br />

		<input type="checkbox" name="danceability_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="danceability_checkbox">Danceability</label>
		<br />

		<input type="checkbox" name="duration_ms_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="duration_ms_checkbox">Duration (ms)</label>
		<br />

		<input type="checkbox" name="energy_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="energy_checkbox">Energy</label>
		<br />

		<input type="checkbox" name="instrumentalness_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="instrumentalness_checkbox">Instrumentalness</label>
		<br />

		<input type="checkbox" name="liveness_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="liveness_checkbox">Liveness</label>
		<br />

		<input type="checkbox" name="loudness_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="loudness_checkbox">Loudness</label>
		<br />

		<input type="checkbox" name="speechiness_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="speechiness_checkbox">Speechiness</label>
		<br />

		<input type="checkbox" name="tempo_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="tempo_checkbox">Tempo</label>
		<br />

		<input type="checkbox" name="valence_checkbox" checked="checked" on:input={updated_checked_values} />
		<label for="valence_checkbox">Valence</label>
		<br />

		<br />



		<h2>Correlation</h2>

		<input type="checkbox" name="correlation_active" checked="checked" on:input={updated_checked_values} />
		<label for="correlation_active">Active</label>
		<br />

		<label for="correlation_method">Correlation Method:</label>
		<select name="correlation_method" on:input={updated_checked_values}>
			<option value="pearson">Pearson</option>
			<option value="spearman">Spearman</option>
			<option value="kendall">Kendall</option>
		</select>

		<br />


		<h2>Timeline</h2>

		<input type="checkbox" name="timeline_active" checked="checked" on:input={updated_checked_values} />
		<label for="timeline_active">Active</label>

		<br />


		<h2>Genre Bar</h2>

		<input type="checkbox" name="genre_bar_active" checked="checked" on:input={updated_checked_values} />
		<label for="genre_bar_active">Active</label>

		<br />


		<h2>Artists</h2>

		<input type="checkbox" name="artists_active" checked="checked" />
		<label for="artists_active">Active</label>

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