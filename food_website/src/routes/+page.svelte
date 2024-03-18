<script lang="ts">
	import type { Recipe } from '$lib';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import type { Folder, RecommendResult, RecommendResults } from '$lib/elasticsearch';
	import CardAndModal from '$lib/recipe_card.svelte';
	/** @type {import('./$types').PageData} */
	export let data: any;
	async function get_recommendations() {
		const result = await fetch('https://34.126.162.255:5000/get_recommendations', {
			credentials: 'include'
		});
		return result.json() as Promise<RecommendResult>;
	}
	let promise = get_recommendations();
	$: folders = data.folder_result.results as Folder[];
	$: other_recommendations = data.other_recommend.results as Recipe[];
	onMount(() => {
		if(!("results" in data.other_recommend)) {
			goto("/login")
		}
	})
</script>

<div class="flex flex-col gap-8 font-serif">
	{#await promise}
		<div class="flex flex-col justify-center items-center p-8 h-96 rounded-md text-3xl gap-4">
			<img
				src="https://i1.sndcdn.com/artworks-hMA1Rw73kK2TDB94-jplCww-t500x500.jpg"
				class="h-64 aspect-auto object-contain"
				alt="whar?"
			/>
			<p class="animate-pulse text-stone-100">Loading...</p>
		</div>
	{:then recommendations}
		{#if Object.entries(recommendations.results).length}
			<div
				class="flex flex-col bg-gradient-to-tr from-fuchsia-600 to-teal-500 rounded-md text-center relative"
				role="listitem"
			>
				<div
					class="absolute top-0 left-0 right-0 bottom-0 bg-[url('https://as2.ftcdn.net/v2/jpg/02/17/70/57/1000_F_217705767_Qs5URQQFJ3dHmqq733X5g9eABkdgWson.jpg')] opacity-15 rounded-md"
				></div>
				<p class="text-3xl text-stone-100 bg-teal-500 p-4 rounded-t-md bg-opacity-25 z-10">
					Recommendations based on <span class="border-2 rounded-md px-2 py-1 font-bold"
						>Your Folders</span
					>
				</p>
				{#if recommendations.results.recommend_from_summary.results.length > 1}
					<div class="grid grid-cols-3 gap-8 p-8 z-10">
						{#each recommendations.results.recommend_from_summary.results as recipe}
							<CardAndModal bind:recipe bind:folders></CardAndModal>
						{/each}
					</div>
				{:else}
					<div class="flex flex-col items-center justify-center h-64 gap-2 opacity-75 z-10">
						<p class="text-stone-900 text-3xl font-bold">
							You have no <span class="border-2 border-stone-900 rounded-md px-2 py-1 font-bold"
								>Bookmark</span
							>
						</p>
						<p class="text-stone-900">Explore in our random section!</p>
					</div>
				{/if}
			</div>
			<div
				class="flex flex-col bg-gradient-to-tr from-rose-400 to-yellow-400 rounded-md text-center relative"
			>
				<div
					class="absolute top-0 left-0 right-0 bottom-0 bg-[url('https://as2.ftcdn.net/v2/jpg/02/17/70/57/1000_F_217705767_Qs5URQQFJ3dHmqq733X5g9eABkdgWson.jpg')] opacity-15 rounded-md"
				></div>
				<p class="text-3xl text-stone-100 bg-yellow-400 p-4 rounded-t-md bg-opacity-25 z-10">
					Recommendations based on <span class="border-2 rounded-md px-2 py-1 font-bold"
						>{recommendations.results.recommend_from_folder.folder_name}</span
					>
				</p>
				{#if recommendations.results.recommend_from_folder.results.length > 1}
					<div class="grid grid-cols-3 gap-8 p-8 z-10">
						{#each recommendations.results.recommend_from_folder.results as recipe}
							<CardAndModal bind:recipe bind:folders></CardAndModal>
						{/each}
					</div>
				{:else}
					<div class="flex flex-col items-center justify-center h-64 gap-2 opacity-75 z-10">
						<p class="text-stone-900 text-3xl font-bold">
							<span class="border-2 border-stone-900 rounded-md px-2 py-1 font-bold"
								>{recommendations.results.recommend_from_folder.folder_name}</span
							> is empty
						</p>
						<p class="text-stone-900">Give it some love!</p>
					</div>
				{/if}
			</div>
			<div
				class="flex flex-col bg-gradient-to-bl from-lime-400 to-teal-500 rounded-md text-center relative"
			>
				<div
					class="absolute top-0 left-0 right-0 bottom-0 bg-[url('https://as2.ftcdn.net/v2/jpg/02/17/70/57/1000_F_217705767_Qs5URQQFJ3dHmqq733X5g9eABkdgWson.jpg')] opacity-15 rounded-md"
				></div>
				<p class="text-3xl text-stone-100 bg-lime-400 p-4 rounded-t-md bg-opacity-25 z-10">
					Recommendations based on <span class="border-2 rounded-md px-2 py-1 font-bold"
						>Random Pick</span
					>
				</p>
				<div class="grid grid-cols-3 gap-8 p-8 z-10">
					{#each recommendations.results.recommend_from_random.results as recipe}
						<CardAndModal bind:recipe bind:folders></CardAndModal>
					{/each}
				</div>
			</div>
			<div
				class="flex flex-col bg-gradient-to-tr from-fuchsia-600 to-yellow-300 rounded-md items-center relative"
			>
				<div
					class="absolute top-0 left-0 right-0 bottom-0 bg-[url('https://as2.ftcdn.net/v2/jpg/02/17/70/57/1000_F_217705767_Qs5URQQFJ3dHmqq733X5g9eABkdgWson.jpg')] opacity-15 rounded-md"
				></div>
				<p
					class="text-3xl text-stone-100 p-4 rounded-t-md bg-opacity-25 border-2 rounded-md px-2 py-1 font-bold mt-8 z-10"
				>
					Top Recipes
				</p>
				<div class="grid grid-cols-3 gap-8 p-8 z-10">
					{#each other_recommendations as recipe}
						<CardAndModal bind:recipe bind:folders></CardAndModal>
					{/each}
				</div>
			</div>
		{:else}
			<div
				class="flex flex-col bg-gradient-to-tr from-fuchsia-600 to-teal-500 rounded-md items-center relative"
			>
				<div
					class="absolute top-0 left-0 right-0 bottom-0 bg-[url('https://as2.ftcdn.net/v2/jpg/02/17/70/57/1000_F_217705767_Qs5URQQFJ3dHmqq733X5g9eABkdgWson.jpg')] opacity-15 rounded-md"
				></div>
				<p
					class="text-3xl text-stone-100 p-4 rounded-t-md bg-opacity-25 border-2 rounded-md px-2 py-1 font-bold mt-8 z-10"
				>
					Explore
				</p>
				<div class="grid grid-cols-3 gap-8 p-8 z-10">
					{#each other_recommendations as recipe}
						<CardAndModal bind:recipe bind:folders></CardAndModal>
					{/each}
				</div>
			</div>
		{/if}
	{:catch}
		<div
			class="flex flex-col bg-gradient-to-tr from-fuchsia-600 to-teal-500 rounded-md items-center relative"
		>
			<div
				class="absolute top-0 left-0 right-0 bottom-0 bg-[url('https://as2.ftcdn.net/v2/jpg/02/17/70/57/1000_F_217705767_Qs5URQQFJ3dHmqq733X5g9eABkdgWson.jpg')] opacity-15 rounded-md"
			></div>
			<p
				class="text-3xl text-stone-100 p-4 rounded-t-md bg-opacity-25 border-2 rounded-md px-2 py-1 font-bold mt-8 z-10"
			>
				Explore
			</p>
			<div class="grid grid-cols-3 gap-8 p-8 z-10">
				{#each other_recommendations as recipe}
					<CardAndModal bind:recipe bind:folders></CardAndModal>
				{/each}
			</div>
		</div>
	{/await}
</div>
