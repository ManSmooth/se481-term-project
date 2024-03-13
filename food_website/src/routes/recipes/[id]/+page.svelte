<script lang="ts">
	import { onMount } from 'svelte';
	import type { SearchResult, Recipe } from '$lib';
	import { parseDuration } from '$lib';

	/** @type {import('./$types').PageData} */
	export let data: any;

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
	$: recipe = data.recipe as Recipe;
	$: ingredients = recipe.RecipeIngredientParts.reduce(
		(obj, k, i) => ({ ...obj, [k]: recipe.RecipeIngredientQuantities[i] }),
		{}
	);
	const capitalize = (str: string, lower = false) =>
		(lower ? str.toLowerCase() : str).replace(/(?:^|\s|["'([{])+\S/g, (match) =>
			match.toUpperCase()
		);
</script>

<div class="flex flex-row gap-8 justify-center font-serif">
	<div
		class="flex flex-col border p-8 border-stone-300 shadow-md justify-between gap-8 bg-stone-200 max-w-6xl w-full"
	>
		<div class="flex flex-col gap-4">
			<div class="flex flex-row gap-2 text-xs opacity-50 flex-wrap">
				{#each recipe.Keywords as keyword}
					<p>
						{keyword}
					</p>
				{/each}
			</div>
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
			<div class="grid grid-cols-[2fr,1fr]">
				<div class="flex flex-row h-96">
					<div class="flex-1 h-full bg-stone-600">
						{#if recipe.Images.length > 0}
							<img src={recipe.Images[0]} class="object-contain w-full h-full" alt="food" />
						{:else}
							<div class=" w-full h-full flex flex-row justify-center items-center">
								<p class="bg-stone-200 px-4 py-2">No Image</p>
							</div>
						{/if}
					</div>
				</div>
				<div class="pl-4 flex flex-row items-center">
					<div
						class="flex flex-col gap-1 justify-around w-full font-sans p-4 h-fit border border-black border-opacity-40 bg-stone-50"
					>
						<p class="text-2xl">Nutrition Info</p>
						<hr class="w-full border-0 border-b border-black border-opacity-50" />
						<div class="pl-4 gap-1 flex flex-col">
							<div class="flex flex-row items-center justify-between">
								<p class="font-bold">Servings</p>
								<p>
									{recipe.RecipeServings ? recipe.RecipeServings : 'Unspecified'}
								</p>
							</div>
							<hr class="w-full border-0 border-b border-black border-opacity-50 border-dashed" />
							<div class="flex flex-row items-center justify-between">
								<p class="font-bold">Yield</p>
								<p>
									{recipe.RecipeYield ? recipe.RecipeYield : 'Unspecified'}
								</p>
							</div>
						</div>
						<hr class="w-full border-0 border-b border-black border-opacity-50" />
						<div class="flex flex-row items-center justify-between">
							<p class="font-bold">Calories</p>
							<p>
								{recipe.Calories} kcal
							</p>
						</div>
						<hr class="w-full border-0 border-b border-black border-opacity-50" />
						<div class="pl-4 gap-1 flex flex-col">
							<div class="flex flex-row items-center justify-between">
								<p>Total Fat</p>
								<p>
									{recipe.FatContent} g
								</p>
							</div>
							<hr class="w-full border-0 border-b border-black border-opacity-50 border-dashed" />
							<div class="flex flex-row items-center justify-between">
								<p>Saturated Fat</p>
								<p>
									{recipe.SaturatedFatContent} g
								</p>
							</div>
						</div>
						<hr class="w-full border-0 border-b border-black border-opacity-50" />
						<div class="flex flex-row items-center justify-between">
							<p class="font-bold">Protein</p>
							<p>
								{recipe.ProteinContent} g
							</p>
						</div>
						<hr class="w-full border-0 border-b border-black border-opacity-50" />
						<div class="flex flex-row items-center justify-between">
							<p class="font-bold">Carbohydrate</p>
							<p>
								{recipe.CarbohydrateContent} g
							</p>
						</div>
						<hr class="w-full border-0 border-b border-black border-opacity-50" />
						<div class="pl-4 gap-1 flex flex-col">
							<div class="flex flex-row items-center justify-between">
								<p>Dietary Fiber</p>
								<p>
									{recipe.FiberContent} g
								</p>
							</div>
							<hr class="w-full border-0 border-b border-black border-opacity-50 border-dashed" />
							<div class="flex flex-row items-center justify-between">
								<p>Sugars</p>
								<p>
									{recipe.SugarContent} g
								</p>
							</div>
						</div>
						<hr class="w-full border-0 border-b border-black border-opacity-50" />
						<div class="flex flex-row items-center justify-between">
							<p class="font-bold">Sodium</p>
							<p>
								{recipe.SodiumContent} mg
							</p>
						</div>
					</div>
				</div>
			</div>
			<div class="flex flex-col gap-4">
				<div>{recipe.Description}</div>
			</div>
			<div class="flex flex-row w-full gap-8">
				<div class="flex flex-col w-96 gap-8 border border-black border-opacity-40 bg-stone-50 p-4 justify-between">
					<div class="flex flex-col w-full place-self-center gap-1">
						<p class="text-2xl">Ingredients</p>
						<hr class="w-full border-0 border-b border-black border-opacity-50" />
						{#each Object.entries(ingredients) as [item, quantity]}
							<div class="flex flex-row justify-between">
								<p>
									{capitalize(item)}
								</p>
								<p>
									{quantity}
								</p>
							</div>
						{/each}
					</div>
					<div class="flex flex-row justify-between items-center">
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
				</div>
				<div class="flex flex-col p-4 flex-1 gap-2">
					<p class="text-2xl">Instructions</p>
					<hr class="w-full border-0 border-b border-black border-opacity-50" />
					{#each recipe.RecipeInstructions as step, i}
						<div class="flex flex-row gap-4">
							<p>{step}</p>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</div>
</div>
