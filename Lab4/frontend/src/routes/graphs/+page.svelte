<script>
	import { getContext, onMount } from 'svelte';
	const FLASK_URL = getContext('flask_url');
	const ID = getContext('id');

	let loading = false;

	let request_dict = {
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
		correlation_method: "pearson",
		id: ID,
	};
	function update_and_fetch() {
		loading = true;

		request_dict.year = document.querySelector('input[name="year_checkbox"]').checked;
		request_dict.popularity = document.querySelector('input[name="popularity_checkbox"]').checked;
		request_dict.acousticness = document.querySelector('input[name="acousticness_checkbox"]').checked;
		request_dict.danceability = document.querySelector('input[name="danceability_checkbox"]').checked;
		request_dict.duration_ms = document.querySelector('input[name="duration_ms_checkbox"]').checked;
		request_dict.energy = document.querySelector('input[name="energy_checkbox"]').checked;
		request_dict.instrumentalness = document.querySelector('input[name="instrumentalness_checkbox"]').checked;
		request_dict.liveness = document.querySelector('input[name="liveness_checkbox"]').checked;
		request_dict.loudness = document.querySelector('input[name="loudness_checkbox"]').checked;
		request_dict.speechiness = document.querySelector('input[name="speechiness_checkbox"]').checked;
		request_dict.tempo = document.querySelector('input[name="tempo_checkbox"]').checked;
		request_dict.valence = document.querySelector('input[name="valence_checkbox"]').checked;
		request_dict.correlation_method = document.querySelector('select[name="correlation_method"]').value;

		let url = FLASK_URL + "/all_graphs" + "?";
		for (let key in request_dict) {
			url += key + "=" + request_dict[key] + "&";
		}

		fetch(url)
			.then(response => response.json())
			.then(data => {
				console.log(data);
				for (let ele_id in data) {
					console.warn(ele_id);
					const ele = document.getElementById(ele_id);
					const graph_b64 = data[ele_id];
					ele.src = "data:image/jpeg;base64," + graph_b64;
				}
				loading = false;
			})
			.catch((error) => {
				console.error('Error:', error);
				loading = false;
			});

		// fetch(FLASK_URL + "/graphs", {
		// 	method: 'POST',
		// 	headers: {
		// 		'Content-Type': 'application/json'
		// 	},
		// 	body: JSON.stringify(checked_values)
		// })
		// 	.then(response => response.json())
		// 	.then(data => {
		// 		console.log(data);
		// 		for (let key in data) {
		// 			console.log(key);
		// 			console.log(data[key]);
		// 		}
		// 		// document.getElementById('right').innerHTML = data.html;
		// 	})
		// 	.catch((error) => {
		// 		console.error('Error:', error);
		// 	});
	}

	onMount(() => {
		update_and_fetch();
	});

</script>

<style>
	div {
		padding: 0.5em;
	}

	img {
		width: 100%;
		height: 100%;
	}

	#holder {
		display: flex;
	}

	#left {
		width: 12.5%;
	}

	#right {
		width: 87.5%;
	}

	#graph_holder {
		display: grid;
		gap: 0;

		padding: 0;

		grid-template-columns: repeat(2, 1fr);
		grid-template-columns: repeat(2, 1fr);

		width: 100%;
		height: 100%;

		justify-self: center;
		align-self: center;
	}
</style>


<div id="holder">
	<div id="left">
		<h1>Graphs</h1>

		<h3>Categories</h3>

		<input type="checkbox" name="year_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="year_checkbox">Year</label>
		<br />

		<input type="checkbox" name="popularity_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="popularity_checkbox">Popularity</label>
		<br />

		<input type="checkbox" name="acousticness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="acousticness_checkbox">Acousticness</label>
		<br />

		<input type="checkbox" name="danceability_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="danceability_checkbox">Danceability</label>
		<br />

		<input type="checkbox" name="duration_ms_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="duration_ms_checkbox">Duration (ms)</label>
		<br />

		<input type="checkbox" name="energy_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="energy_checkbox">Energy</label>
		<br />

		<input type="checkbox" name="instrumentalness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="instrumentalness_checkbox">Instrumentalness</label>
		<br />

		<input type="checkbox" name="liveness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="liveness_checkbox">Liveness</label>
		<br />

		<input type="checkbox" name="loudness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="loudness_checkbox">Loudness</label>
		<br />

		<input type="checkbox" name="speechiness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="speechiness_checkbox">Speechiness</label>
		<br />

		<input type="checkbox" name="tempo_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="tempo_checkbox">Tempo</label>
		<br />

		<input type="checkbox" name="valence_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="valence_checkbox">Valence</label>
		<br />

		<br />


		<h2>Correlation</h2>

		<label for="correlation_method">Method:</label>
		<select name="correlation_method" on:input={update_and_fetch}>
			<option value="pearson">Pearson</option>
			<option value="spearman">Spearman</option>
			<option value="kendall">Kendall</option>
		</select>

		<br />


		<br />
		<hr />

		<p>Loading: {loading}</p>


		<hr />
		<br />
		
		<a href="/">
			<button>Back to Home</button>
		</a>

	</div>

	<div id="right">
		<div id="graph_holder">
			<img id="heat_map" alt="Heat Map" />
			<img id="time_line" alt="Time Line" />
			<img id="artists" alt="Artists Bar Graph" />
			<img id="genre_bar" alt="Genre Bar Graph" />
		</div>
	</div>
</div>