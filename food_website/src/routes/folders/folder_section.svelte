<script lang="ts">
	import type { Folder, Recipe, SearchResult } from '$lib/elasticsearch';
	import CardAndModal from '$lib/recipe_card.svelte';

	export let folder: Folder;
	export let folders: Folder[];
	let recommend_open = false;
	async function get_recommendations() {
		const result = await fetch(
			`https://34.126.162.255:5000/folder_recommend?folder_index=${folder.index}`,
			{
				credentials: 'include'
			}
		);
		return result.json() as Promise<SearchResult>;
	}
	$: promise = recommend_open ? get_recommendations() : { results: [] };
</script>

<div
	class="border border-black border-opacity-30 bg-stone-700 flex flex-col gap-2 min-h-64 rounded-lg w-full relative"
>
	<div
		class="flex flex-col px-8 py-4 bg-gradient-to-r from-blue-600 to-teal-400 rounded-t-lg relative"
	>
		<div
			class="absolute top-0 left-0 right-0 bottom-0 bg-[url('https://as2.ftcdn.net/v2/jpg/02/17/70/57/1000_F_217705767_Qs5URQQFJ3dHmqq733X5g9eABkdgWson.jpg')] opacity-15 rounded-md"
		></div>
		<p class="text-2xl text-white">{folder.folder_name}</p>
	</div>
	{#if folder.recipes.length > 0}
		<div class="grid grid-cols-3 gap-8 p-8 z-10">
			{#each folder.recipes as recipe}
				<CardAndModal bind:recipe bind:folders />
			{/each}
			<button
				class="h-64 w-full p-8 border-2 opacity-30 border-dashed border-stone-100 text-stone-100 rounded-md flex flex-row justify-center items-center hover:opacity-100 transition-all duration-300 font-sans"
				on:click={() => (recommend_open = !recommend_open)}
			>
				<div class="flex flex-col items-center">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						class="w-12 h-12"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
					</svg>
					<p>Recommend new dishes</p>
				</div>
			</button>
		</div>
	{:else}
		<div class="flex flex-col justify-center items-center flex-1">
			<p class="text-2xl opacity-50">Empty Folder</p>
		</div>
	{/if}
	{#if recommend_open}
		<div class="z-20 absolute top-full w-full p-4">
			<div
				class="w-full h-full bg-stone-700 flex flex-col gap-2 border-2 border-transparent bg-clip-border bg-gradient-to-br from-rose-400 to-yellow-200"
			>
				<div class="w-full h-full bg-stone-700 flex flex-col p-8 gap-8">
					<p class="text-white text-2xl">
						Recommendations for <span class="border-2 rounded-md px-2 py-1 font-bold"
							>{folder.folder_name}</span
						>
					</p>
					{#await promise}
						<div class="flex flex-col w-full h-64 text-center justify-center">
							<p class="text-xl text-stone-100 opacity-25 animate-pulse">
								Generating your recommendations!
							</p>
						</div>
					{:then result}
						<div class="grid grid-cols-3 gap-8 z-10">
							{#each result.results as recipe}
								<CardAndModal bind:recipe bind:folders />
							{/each}
						</div>
					{/await}
				</div>
			</div>
		</div>
	{/if}
</div>
