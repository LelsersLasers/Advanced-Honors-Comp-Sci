<script>
	import { setContext } from 'svelte';

	const FLASK_URL_BASE = 'http://localhost:';
	setContext('flask_url_base', FLASK_URL_BASE);

	const ID = btoa(Math.random().toString());
	setContext('id', ID);
</script>

<slot />