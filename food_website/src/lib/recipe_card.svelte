<script lang="ts">
	import { type Recipe } from '$lib';
	import type { Folder } from './elasticsearch';
	import Modal from '$lib/recipe_modal.svelte';
	let modalShowing = false;
	export let recipe: Recipe;
	export let folders: Folder[];
	const capitalize = (str: string, lower = false) =>
		(lower ? str.toLowerCase() : str).replace(/(?:^|\s|["'([{])+\S/g, (match) =>
			match.toUpperCase()
		);
	const parser = new DOMParser();
	const htmlParse = (text: string) => parser.parseFromString(text, 'text/html').body.innerText;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<Modal bind:modalShowing bind:recipe bind:folders></Modal>
<button
	on:click={() => (modalShowing = true)}
	class="h-64 flex flex-row text-left border rounded-md p-8 border-stone-900 border-opacity-30 gap-2 items-stretch bg-stone-200 transition-all hover:shadow-lg hover:scale-105 font-serif"
>
	<div class="aspect-square bg-stone-600 shadow-md">
		{#if recipe.Images[0]}
			<img src={recipe.Images[0]} class="object-cover w-full h-full" alt={recipe.Name} />
		{:else}
			<div class="w-full h-full flex flex-row items-center justify-center text-stone-100">
				<p>No Image</p>
			</div>
		{/if}
	</div>
	<div class="flex flex-col justify-between w-full">
		<div class="flex flex-col gap-2 w-full">
			<div class="flex flex-col">
				{#if recipe.rating}
					<p class="text-sm">
						(Rated: {recipe.rating}★)
					</p>
				{/if}
				<p class="text-2xl">
					{capitalize(htmlParse(recipe.Name))}
				</p>
				<p class="text-sm">
					{recipe.AuthorName}
				</p>
				<div class="flex flex-row justify-between w-full">
					<div class="flex flex-row gap-1 items-baseline text-sm">
						<p>
							{'★'.repeat(Math.floor(recipe.AggregatedRating))}{'☆'.repeat(
								5 - Math.floor(recipe.AggregatedRating)
							)}
						</p>
						<p>
							{recipe.AggregatedRating ? recipe.AggregatedRating : 0.0}
						</p>
						<p class="opacity-50">
							({recipe.ReviewCount})
						</p>
					</div>
					<p class="opacity-50">
						{new Date(recipe.DatePublished).toISOString().split('T')[0]}
					</p>
				</div>
			</div>
		</div>
		<div class="flex flex-col gap-4 w-full">
			<div class="flex flex-row gap-2 text-xs opacity-50 flex-wrap">
				{#each recipe.Keywords as keyword}
					<p>
						{keyword}
					</p>
				{/each}
			</div>
		</div>
	</div>
</button>
