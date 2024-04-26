<script>
	import { onMount } from 'svelte';

	function change_method(e) {
		const method = e.target.value;
		const query = window.location.search;
		const url = "/recommendations/" + method + query;
		window.location = url;
	}

	function change_dist(e) {
		const dist = e.target.value;

		// add/replace as query parameter
		const now_url = window.location.href;
		const url = new URL(now_url);
		url.searchParams.set("dist", dist);
		window.location = url;
	}

	onMount(() => {
		let url = window.location.href;
		let method = url.split("/").pop();
		if (method) {
			document.getElementById("method").value = method;
		}

		let dist = url.split("dist=").pop();
		if (dist) {
			document.getElementById("dist").value = dist;
		}
	});

</script>

<a href="/">
	<button>Back to Home</button>
</a>

<br />

<h2>Method</h2>

<label for="method">Method:</label>
<select id="method" name="method" on:input={change_method}>
	<option value="" disabled selected="selected">Select--</option>
	<option value="cnn">CNN</option>
	<option value="autoencoder">Autoencoder</option>
	<option value="predictor">Predictor</option>
	<option value="simple">Simple</option>
</select>

<label for="dist">Distance Function:</label>
<select id="dist" name="dist" on:input={change_dist}>
	<option value="" disabled selected="selected">Select--</option>
	<option value="cos">Cosine Similarity</option>
	<option value="mae">Mean Absolute Difference</option>
	<option value="mse">Mean Squared Difference</option>
	<option value="euclidean">Euclidean Distance</option>
	<option value="dot">Dot Product</option>
</select>

<slot />