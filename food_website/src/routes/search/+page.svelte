<script lang="ts">
	import { onMount } from 'svelte';
	import type { Recipe } from '$lib';
	import { goto } from '$app/navigation';
	import type { Folder } from '$lib/elasticsearch';
	import CardAndModal from '$lib/recipe_card.svelte';

	/** @type {import('./$types').PageData} */
	export let data: any;
	$: recipes = data.result.results as Recipe[];
	$: suggestion = data.suggest_result.suggest as string;
	$: folders = data.folder_result.results as Folder[];
	$: query = data.query as string;
	onMount(() => {
		if (!('results' in data.result)) {
			goto('/login');
		}
	});
</script>

{#if query !== suggestion && suggestion !== undefined}
	<div class="bg-stone-200 p-4">
		Did you mean: <a
			href="/search?query={suggestion}"
			class="text-lime-600 underline hover:text-lime-800">{suggestion}</a
		>.
	</div>
{/if}
<div class="grid grid-cols-3 gap-8">
	{#if recipes}
		{#each recipes as recipe}
			<CardAndModal bind:recipe bind:folders></CardAndModal>
		{/each}
	{/if}
</div>
