<script lang="ts">
	import type { SearchResult, Recipe } from '$lib';
	import { parseDuration } from '$lib';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let recommended: SearchResult;
	/** @type {import('./$types').PageData} */
	export let data: any;
	$: recipes = data.recommended.results as Recipe[];
	const capitalize = (str: string, lower = false) =>
		(lower ? str.toLowerCase() : str).replace(/(?:^|\s|["'([{])+\S/g, (match) =>
			match.toUpperCase()
		);
	$: formatDateTime = (duration_string: string) => {
		const duration = parseDuration(duration_string);
		let str = '';
		str += duration.years ? duration.years + 'Year ' : '';
		str += duration.months ? duration.months + 'Month ' : '';
		str += duration.weeks ? duration.weeks + 'W ' : '';
		str += duration.days ? duration.days + 'D ' : '';
		str += duration.hours ? duration.hours + 'H ' : '';
		str += duration.minutes ? duration.minutes + 'M ' : '';
		str += duration.seconds ? duration.seconds + 'S ' : '';
		return str.trim();
	};
	onMount(() => {
		if(!recipes) {
			goto("/login", {
				invalidateAll: true
			})
		}
	})
</script>

<div class="grid grid-cols-3 gap-8">
	{#if recipes}
		{#each recipes as recipe}
			<a
				href="/recipes/{recipe.RecipeId}"
				class="flex flex-col border rounded-md p-8 border-stone-300 shadow-md justify-between gap-8 bg-stone-200"
			>
				<div class="flex flex-col gap-4">
					<div class="flex flex-col">
						<p class="text-3xl">
							{recipe.Name}
						</p>
						<p>
							{recipe.AuthorName}
						</p>
						<div class="flex flex-row justify-between w-full">
							<div class="flex flex-row gap-1 items-baseline">
								<p>
									{'★'.repeat(Math.floor(recipe.AggregatedRating))}{'☆'.repeat(
										5 - Math.floor(recipe.AggregatedRating)
									)}
								</p>
								<p>
									{recipe.AggregatedRating.toFixed(2)}
								</p>
								<p class="opacity-50">
									({recipe.ReviewCount})
								</p>
							</div>
							<p class="opacity-50">
								{recipe.DatePublished.split('T')[0]}
							</p>
						</div>
					</div>
					<div class="h-96 w-full bg-stone-600">
						{#if recipe.Images.length > 0}
							<img src={recipe.Images[0]} class="object-cover w-full h-full" alt="food" />
						{:else}
							<div class=" w-full h-full flex flex-row justify-center items-center">
								<p class="bg-stone-400 px-4 py-2">No Image</p>
							</div>
						{/if}
					</div>
					<!-- <p>
								{recipe.Description}
							</p> -->
				</div>
				<div class="flex flex-col gap-4">
					<div class="flex flex-row gap-2 justify-around w-full font-sans">
						<div class="flex flex-col items-center">
							<p class="text-xs">Cook Time</p>
							<p class="text-xl">
								{formatDateTime(recipe.CookTime)}
							</p>
						</div>
						<div class="flex flex-col items-center">
							<p class="text-xs">Prep Time</p>
							<p class="text-xl">
								{formatDateTime(recipe.PrepTime)}
							</p>
						</div>
						<div class="flex flex-col items-center">
							<p class="text-xs">Total Time</p>
							<p class="text-xl">
								{formatDateTime(recipe.TotalTime)}
							</p>
						</div>
					</div>
					<div class="flex flex-row gap-2 text-xs opacity-50 flex-wrap">
						{#each recipe.Keywords as keyword}
							<p>
								{keyword}
							</p>
						{/each}
					</div>
				</div>
			</a>
		{/each}
	{/if}
</div>
