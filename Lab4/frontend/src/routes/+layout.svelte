<script>
	import { setContext } from 'svelte';
	setContext('flask_url', 'http://localhost:5000/flask');
</script>

<slot />