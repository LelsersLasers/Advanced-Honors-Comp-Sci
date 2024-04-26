<script>
	import { onMount } from 'svelte';

	function change_method(e) {
		const method = e.target.value;
		const url = "/recommendations/" + method;
		window.location = url;
	}

	onMount(() => {
		let url = window.location.href;
		let method = url.split("/").pop();
		if (method) {
			document.getElementById("method").value = method;
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
<select id="dist" name="dist" on:input={change_method}>
	<option value="" disabled selected="selected">Select--</option>
	<option value="cnn">CNN</option>
	<option value="autoencoder">Autoencoder</option>
	<option value="predictor">Predictor</option>
	<option value="simple">Simple</option>
</select>

<slot />