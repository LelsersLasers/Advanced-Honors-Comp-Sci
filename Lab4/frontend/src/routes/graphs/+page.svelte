<script>
	import { getContext, onMount } from 'svelte';
	const FLASK_URL = getContext('flask_url');
	const ID = getContext('id');

	let loading_initial = {
		"heat_map": true,
		"time_line": true,
		"artists": true,
		"genre_bar": true,
	};
	
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
		let keys = Object.keys(loading_initial);

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

		const old_correlation_method = request_dict.correlation_method;
		request_dict.correlation_method = document.querySelector('select[name="correlation_method"]').value;
		if (request_dict.correlation_method != old_correlation_method) {
			keys = ["heat_map"];
		}

		for (let i in keys) {
			const key = keys[i];

			let url = FLASK_URL + "graphs_bs64/" + key + "?";

			for (let k in request_dict) {
				url += k + "=" + request_dict[k] + "&";
			}

			fetch(url)
				.then(response => response.json())
				.then(data => {
					const ele = document.getElementById(key);
					const graph_b64 = data["graph"];
					ele.src = "data:image/jpeg;base64," + graph_b64;
					ele.style.display = "block";
					loading_initial[key] = false;
				})
				.catch((error) => {
					console.error('Error:', error);
					loading_initial[key] = false;
				});
		}
	}

	onMount(() => {
		update_and_fetch();
	});

</script>

<svelte:head>
	<title>Graphs</title>
</svelte:head>


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

		justify-self: center;
		align-self: center;
	}

	.image_placeholder {
		display: flex;
		justify-content: center;
	}

	.loader {
		border: 16px solid #f3f3f3;
		border-top: 16px solid #3498db;
		border-radius: 50%;
		width: 80px;
		height: 80px;
		animation: spin 2s linear infinite;
		margin: 2em;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}


</style>


<div id="holder">
	<div id="left">
		<h1>Graphs</h1>

		<h3>Categories</h3>

		<input type="checkbox" id="year_checkbox" name="year_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="year_checkbox">Year</label>
		<br />

		<input type="checkbox" id="popularity_checkbox" name="popularity_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="popularity_checkbox">Popularity</label>
		<br />

		<input type="checkbox" id="acousticness_checkbox" name="acousticness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="acousticness_checkbox">Acousticness</label>
		<br />

		<input type="checkbox" id="danceability_checkbox" name="danceability_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="danceability_checkbox">Danceability</label>
		<br />

		<input type="checkbox" id="duration_ms_checkbox" name="duration_ms_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="duration_ms_checkbox">Duration (ms)</label>
		<br />

		<input type="checkbox" id="energy_checkbox" name="energy_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="energy_checkbox">Energy</label>
		<br />

		<input type="checkbox" id="instrumentalness_checkbox" name="instrumentalness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="instrumentalness_checkbox">Instrumentalness</label>
		<br />

		<input type="checkbox" id="liveness_checkbox" name="liveness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="liveness_checkbox">Liveness</label>
		<br />

		<input type="checkbox" id="loudness_checkbox" name="loudness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="loudness_checkbox">Loudness</label>
		<br />

		<input type="checkbox" id="speechiness_checkbox" name="speechiness_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="speechiness_checkbox">Speechiness</label>
		<br />

		<input type="checkbox" id="tempo_checkbox" name="tempo_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="tempo_checkbox">Tempo</label>
		<br />

		<input type="checkbox" id="valence_checkbox" name="valence_checkbox" checked="checked" on:input={update_and_fetch} />
		<label for="valence_checkbox">Valence</label>
		<br />

		<br />


		<h2>Correlation</h2>

		<label for="correlation_method">Method:</label>
		<select id="correlation_method" name="correlation_method" on:input={update_and_fetch}>
			<option value="pearson">Pearson</option>
			<option value="spearman">Spearman</option>
			<option value="kendall">Kendall</option>
		</select>

		<br />

		<br />
		<hr />
		<br />
		
		<a href="/">
			<button>Back to Home</button>
		</a>

	</div>

	<div id="right">
		<div id="graph_holder">
			{#if loading_initial["heat_map"]}
				<div class="image_placeholder">
					<div class="loader"></div>
				</div>
			{/if}
			<img id="heat_map" alt="Heat Map" style="display: none" />

			{#if loading_initial["time_line"]}
			<div class="image_placeholder">
				<div class="loader"></div>
			</div>
			{/if}
			<img id="time_line" alt="Heat Map" style="display: none" />

			{#if loading_initial["artists"]}
			<div class="image_placeholder">
				<div class="loader"></div>
			</div>
			{/if}
			<img id="artists" alt="Heat Map" style="display: none" />

			{#if loading_initial["genre_bar"]}
			<div class="image_placeholder">
				<div class="loader"></div>
			</div>
			{/if}
			<img id="genre_bar" alt="Heat Map" style="display: none" />
		</div>
	</div>
</div>