<script>
	import { getContext,  } from 'svelte';
	const FLASK_URL = getContext('flask_url');

	let input_type = "upload";

	let search_results;


	let search_term = "";
	function search_spotify() {
		const url = FLASK_URL + "spotify/search/" + search_term;
		fetch(url)
			.then(response => response.json())
			.then(data => {
				search_results = data.map(item => {
					const name = item.name;
					const authors = item.artists.map(artist => artist.name).join(", ");
					const id = item.id;
					return { name, authors, id };
				});
			});
	}

	let fetch_id = "";
	function fetch_spotify() {
		
	}
	
</script>

<svelte:head>
	<title>Recommendations CNN</title>
</svelte:head>


<h2>Input</h2>

<label for="input">Input:</label>
<select id="input" name="input" bind:value={input_type}>
	<option value="upload">Image Upload</option>
	<option value="spotify_search">Spotify Search</option>
	<option value="spotify_id">Spotify ID</option>
</select>

<br />
<br />


{#if input_type == "upload"}
	<input type="file" id="file" name="file" accept="image/*" />
{:else if input_type == "spotify_search"}
	<label for="search">Search:</label>
	<input type="text" id="search" name="search" bind:value={search_term} />
	<button on:click={search_spotify}>Search</button>

	{#if search_results}
		{#if search_results.length == 0}
			<p>No results found</p>
		{:else}
			<h2>Results</h2>
			<ul>
				{#each search_results as result (result.id)}
					<li>{result.name} by {result.authors}</li>
				{/each}
			</ul>
		{/if}
	{/if}
{:else if input_type == "spotify_id"}
	<label for="id">ID:</label>
	<input type="text" id="id" name="id" bind:value={fetch_id} />
	<button on:click={fetch_spotify}>Fetch</button>
{/if}