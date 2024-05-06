<script>
	import { getContext } from 'svelte';
	const FLASK_URL = getContext('flask_url');

	let model = "predictor";
	let dist = "cos";
	let input_type = "spotify_search";
	let google_mode = true;

	let results = [];

	let loading = false;


	let search_results = [];
	let invalid_id = true;
	let fetch_info = {
		"name": "",
		"artists": "",
		"index": -1,
	}

	$: {
		if (input_type == "upload" && model != "cnn") {
			input_type = "spotify_id";
		}
	}

	let search_term = "";
	function search_spotify() {
		loading = true;
		const search_query = encodeURIComponent(search_term)

		const url = FLASK_URL + "spotify/search/" + search_query;
		fetch(url)
			.then(response => response.json())
			.then(data => {
				search_results = data;
				loading = false;
			});
	}

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
	function select_song(index) {
		fetch_info = search_results.find(x => x["index"] == index);
		fetch_id = fetch_info["id"];
		invalid_id = false;
		search_results = [];
	}

	let image_b64 = "";
	let input_b64 = "";
	function upload() {
		const file = document.getElementById("file").files[0];
		const reader = new FileReader();
		fetch_info = {
			"name": "Uploaded Image",
			"artists": "",
			"index": -1,
		}
		reader.onload = function() {
			image_b64 = reader.result;
			input_b64 = image_b64.split(",")[1];
		}
		reader.readAsDataURL(file);
	}


	function go_button() {		
		if (input_type == "spotify_id") {
			if (invalid_id) {
				return;
			}
		}

		loading = true;

		const url = FLASK_URL + "recommendations";
		fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				"model": model,
				"dist": dist,
				"input_type": input_type,
				"google_mode": google_mode,
				"image_b64": input_b64,
				"index": fetch_info["index"],
			}),
		})
			.then(response => response.json())
			.then(data => {
				results = data;
				loading = false;
			});

		// let url = FLASK_URL + "recommendations/";
		// url += model + "/"
		// url += dist + "/";
		// url += fetch_info["index"] + "/";
		// url += google_mode;
		// url += "?image_b64=" + input_b64;

		// fetch(url)
		// 	.then(response => response.json())
		// 	.then(data => {
		// 		results = data;
		// 		loading = false;
		// 	});
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
	<option value="spotify_search" selected="selected">Spotify Search</option>
	<option value="spotify_id">Spotify ID</option>
	<option value="upload">Image Upload (CNN only)</option>
</select>


{#if model == "cnn"}
	<br />

	<label for="google_mode">Google Mode (CNN only):</label>
	<input type="checkbox" id="google_mode" name="google_mode" bind:checked={google_mode} />
{/if}


{#if input_type == "spotify_search"}
	<h3>Spotify Search</h3>

	<label for="search_term">Search Title:</label>
	<input type="text" id="search_term" name="search_term" bind:value={search_term} />

	<button on:click={search_spotify}>Search</button>

	{#if search_results.length > 0}
		<h3>Search Results</h3>
		<ul>
			{#each search_results as result}
				<li>
					{result["name"]} by {result["artists"]}
					<button on:click={() => select_song(result["index"])}>Select</button>
				</li>
			{/each}
		</ul>
	{/if}
{:else if input_type == "spotify_id"}

	<h3>Spotify ID</h3>

	<label for="fetch_id">Spotify ID:</label>
	<input type="text" id="fetch_id" name="fetch_id" bind:value={fetch_id} />

	<button on:click={fetch_spotify}>Fetch</button>
{:else if input_type == "upload"}

	<h3>Image Upload</h3>

	<input type="file" id="file" name="file" accept="image/*" />

	<button on:click={upload}>Upload</button>
{/if}


{#if input_type == "spotify_id" || input_type == "spotify_search"}
	<h2>Selected Song</h2>

	{#if invalid_id}
		<p>Invalid ID</p>
	{/if}
	{#if fetch_info["index"] != -1}
		<p>{fetch_info["name"]} by {fetch_info["artists"]} (index: {fetch_info["index"]})</p>
	{/if}
{:else if input_type == "upload"}
	<h2>Uploaded Image</h2>

	{#if image_b64 != ""}
		<img src={image_b64} width="128" height="128" />
	{/if}
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