<script>
	import { setContext } from 'svelte';

	const FLASK_URL = 'http://localhost:5000/';
	setContext('flask_url', FLASK_URL);

	const ID = btoa(Math.random().toString());
	setContext('id', ID);
</script>

<slot />