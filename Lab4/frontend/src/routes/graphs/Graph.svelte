<script>
    export let name;
    export let loading_initial;
    export let graph_b64;
    $: {
        if (!loading_initial) {
            const ele = document.getElementById("graph_" + name);
            ele.src = "data:image/jpeg;base64," + graph_b64;
            ele.style.display = "block";
        }
    
    }
</script>

<style>
    img {
        width: 100%;
        height: 100%;
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


{#if loading_initial}
    <div class="image_placeholder">
        <div class="loader"></div>
    </div>
{/if}
<img id={"graph_" + name} alt={name} style="display: none" />