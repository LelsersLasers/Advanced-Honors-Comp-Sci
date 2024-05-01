<script>
	import { getContext, onMount } from 'svelte';
	const FLASK_URL = getContext('flask_url');
	// let token;

	let model = "predictor";
	let dist = "cos";
	let input_type = "spotify_id";
	let google_mode = true;

	let results = [];

	let loading = false;


	// let search_results = null;
	let invalid_id = true;
	let fetch_info = {
		"name": "",
		"artists": "",
		"index": -1,
	}


	onMount(() => {
		console.log(FLASK_URL);
		// connect();
	});

	// function connect() {
	// 	const url = FLASK_URL + "spotify/token";
	// 	fetch(url)
	// 		.then(response => response.json())
	// 		.then(data => {
	// 			token = data['access_token'];
	// 		});
	// }

	// let search_term = "";
	// function search_spotify() {
	// 	const search_query = search_term.replace(" ", "%20");

	// 	let url = "https://api.spotify.com/v1/search";
	// 	url += "?q=" + search_query;
	// 	url += "&type=track";
	// 	url += "&limit=10";


	// 	fetch(url, {
	// 		method: "GET",
	// 		headers: {
	// 			"Authorization": "Bearer " + token
	// 		},
	// 	})
	// 		.then(response => response.json())
	// 		.then(data => {
	// 			search_results = data.tracks.items.map(item => {
	// 				const name = item.name;
	// 				const authors = item.artists.map(artist => artist.name).join(", ");
	// 				const id = item.id;
	// 				return { name, authors, id };
	// 			});
	// 		});

	// 	// const url = FLASK_URL + "spotify/search/" + search_term;
	// 	// fetch(url)
	// 	// 	.then(response => response.json())
	// 	// 	.then(data => {
	// 	// 		search_results = data.map(item => {
	// 	// 			const name = item.name;
	// 	// 			const authors = item.artists.map(artist => artist.name).join(", ");
	// 	// 			const id = item.id;
	// 	// 			return { name, authors, id };
	// 	// 		});
	// 	// 	});
	// }

	let fetch_id = "";
	function fetch_spotify() {
		loading = true;
		const test_valid_id_url = FLASK_URL + "spotify/fetch/" + fetch_id;
		fetch(test_valid_id_url)
			.then(response => response.json())
			.then(data => {
				console.log(data);
				fetch_info = data;
				invalid_id = fetch_info["data"] == -1;
				loading = false;
			});
	}
	// function fetch_button(id) {
	// 	fetch_id = id;
	// 	fetch_spotify();
	// }


	function go_button() {		
		if (input_type == "spotify_id") {
			if (invalid_id) {
				return;
			}
		}

		loading = true;

		let url = FLASK_URL + "recommendations/";
		url += model + "/"
		url += dist + "/";
		url += fetch_info["index"] + "/";
		url += google_mode;

		fetch(url)
			.then(response => response.json())
			.then(data => {
				results = data;
				loading = false;
			});
	}

</script>





<svelte:head>
	<title>Recommendations Home</title>
</svelte:head>


<a href="/">
	<button>Back to Home</button>
</a>

{#if loading}
	<p>Loading...</p>
{/if}

<br />

<h2>Method</h2>

<label for="model">Model:</label>
<select id="model" name="model" bind:value={model}>
	<option value="predictor" selected="selected">Predictor</option>
	<option value="autoencoder">Autoencoder</option>
	<option value="simple">Simple</option>
	<option value="cnn">CNN</option>
</select>

<br />

<label for="dist">Distance Function:</label>
<select id="dist" name="dist" bind:value={dist}>
	<option value="cos" selected="selected">Cosine Similarity</option>
	<option value="mae">Mean Absolute Difference</option>
	<option value="mse">Mean Squared Difference</option>
	<option value="euclidean">Euclidean Distance</option>
	<option value="dot">Dot Product</option>
</select>

<br />
<br />

<h2>Input</h2>

<label for="input">Input:</label>
<select id="input" name="input" bind:value={input_type}>
	<!-- <option value="spotify_search">Spotify Search</option> -->
	<option value="spotify_id" selected="selected">Spotify ID</option>
	<option value="upload">Image Upload (CNN only)</option>
</select>


{#if model == "cnn"}
	<br />

	<label for="google_mode">Google Mode (CNN only):</label>
	<input type="checkbox" id="google_mode" name="google_mode" bind:checked={google_mode} />
{/if}


<!-- {#if input_type == "spotify_search"}
	<h3>Spotify Search</h3>

	<label for="search_term">Search Term:</label>
	<input type="text" id="search_term" name="search_term" bind:value={search_term} />

	<button on:click={search_spotify}>Search</button>

	{#if search_results}
		{#if search_results.length > 0}
			<h3>Results</h3>
			<ul>
				{#each search_results as result}
					<li>
						{result.name} by {result.authors}
						<button on:click={() => fetch_button(result.id)}>Fetch</button>
					</li>
				{/each}
			</ul>
		{:else}
			<p>No results found</p>
		{/if}
	{/if} -->
{#if input_type == "spotify_id"}

	<h3>Spotify ID</h3>

	<label for="fetch_id">Spotify ID:</label>
	<input type="text" id="fetch_id" name="fetch_id" bind:value={fetch_id} />

	<button on:click={fetch_spotify}>Fetch</button>

	{#if invalid_id}
		<p>Invalid ID</p>
	{/if}
	{#if fetch_info["index"] != -1}
		<p>{fetch_info["name"]} by {fetch_info["artists"]} (index: {fetch_info["index"]})</p>
	{/if}

{:else if input_type == "upload"}

	<h3>Image Upload</h3>

	<input type="file" id="file" name="file" accept="image/*" />

	<button>Upload</button>
{/if}


<h1>GO</h1>

<button on:click={go_button}>Go</button>

<h1>Results</h1>

{#if results.length > 0}
	<ol>
		{#each results as result}
			<li>
				{result["name"]} by {result["artists"]} (dist: {result["dist"]})
			</li>
		{/each}
	</ol>
{:else}
	<p>No results</p>
{/if}



<!-- {#if model == "cnn"}

{:else if model == "autoencoder"}

{:else if model == "predictor"}

{:else if model == "simple"}

{/if} -->