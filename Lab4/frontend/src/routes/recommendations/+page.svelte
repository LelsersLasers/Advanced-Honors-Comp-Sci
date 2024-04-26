<script>
	let method = "cnn";
	let dist = "cos";


</script>





<svelte:head>
	<title>Recommendations Home</title>
</svelte:head>


<a href="/">
	<button>Back to Home</button>
</a>

<br />

<h2>Method</h2>

<label for="method">Method:</label>
<select id="method" name="method" bind:value={method}>
	<option value="cnn" selected="selected">CNN</option>
	<option value="autoencoder">Autoencoder</option>
	<option value="predictor">Predictor</option>
	<option value="simple">Simple</option>
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