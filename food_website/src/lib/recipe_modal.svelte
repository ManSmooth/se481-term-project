<script lang="ts">
	import { invalidate, invalidateAll } from '$app/navigation';
	import { parseDuration, type Recipe } from '$lib';
	import type { Folder } from './elasticsearch';

	export let modalShowing: boolean = false;
	export let recipe: Recipe;
	export let folders: Folder[];
	let toggleBookmark = false;
	const getIngredients = (recipe: Recipe) => {
		return recipe.RecipeIngredientParts.reduce(
			(obj, k, i) => ({ ...obj, [k]: recipe.RecipeIngredientQuantities[i] }),
			{}
		);
	};
	const capitalize = (str: string, lower = false) =>
		(lower ? str.toLowerCase() : str).replace(/(?:^|\s|["'([{])+\S/g, (match) =>
			match.toUpperCase()
		);
	const formatDateTime = (duration_string: string) => {
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

	let folder_index = -1;
	let rating = 0;
	$: submittable = folder_index > -1 && rating >= 1 && rating <= 5;
	function submitForm() {
		fetch('https://34.126.162.255:5000/bookmark', {
			method: 'POST',
			body: JSON.stringify({
				folder_index,
				recipe_id: recipe.RecipeId,
				rating
			}),
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		}).then((res) => {
			toggleBookmark = false;
			invalidate("https://34.126.162.255:5000/folders");
		});
	}

	let dialog: HTMLDialogElement; // HTMLDialogElement

	$: if (dialog && modalShowing) dialog.showModal();
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
	bind:this={dialog}
	on:close={() => (modalShowing = false)}
	on:click|self={() => dialog.close()}
	class="max-w-full p-0"
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div on:click|stopPropagation>
		<button
			class="absolute top-4 right-4 bg-lime-300 px-2 py-1 border border-black"
			on:click={() => dialog.close()}>Close</button
		>
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
						{capitalize(recipe.Name)}
					</p>
					<p>
						{recipe.AuthorName}
					</p>
					<div class="flex flex-row justify-between w-full">
						<div class="flex flex-row gap-1 items-center">
							<p>
								{'★'.repeat(Math.floor(recipe.AggregatedRating))}{'☆'.repeat(
									5 - Math.floor(recipe.AggregatedRating)
								)}
							</p>
							<p>
								{recipe.AggregatedRating}
							</p>
							<p class="opacity-50">
								({recipe.ReviewCount})
							</p>
							<div class="flex flex-row gap-2 items-center">
								<button on:click={() => (toggleBookmark = !toggleBookmark)}>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										fill="none"
										viewBox="0 0 24 24"
										stroke-width="1.5"
										stroke="currentColor"
										class="w-4 h-4 hover:fill-lime-400 hover:text-lime-600"
										class:fill-lime-400={toggleBookmark}
										class:text-lime-600={toggleBookmark}
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0 1 11.186 0Z"
										/>
									</svg>
								</button>
								{#if toggleBookmark}
									<form class="flex flex-row gap-2" on:submit|preventDefault={submitForm}>
										<select bind:value={folder_index} placeholder="Folder">
											<option disabled value="-1"> Select a folder </option>
											{#each folders as folder}
												<option value={folder.index}>
													{folder.folder_name}
												</option>
											{/each}
										</select>
										<input
											class="min-w-24"
											type="number"
											max="5"
											min="1"
											placeholder="Rating"
											bind:value={rating}
										/>
										<button
											disabled={!submittable}
											type="submit"
											class="disabled:text-black text-lime-600"
											class:underline={submittable}>Submit</button
										>
									</form>
								{/if}
							</div>
						</div>
						<p class="opacity-50">
							{new Date(recipe.DatePublished).toISOString().split('T')[0]}
						</p>
					</div>
				</div>
				<div class="grid grid-cols-[2fr,1fr]">
					<div class="flex flex-row h-96">
						<div class="flex-1 h-full bg-stone-600">
							{#if recipe.Images.length > 0}
								<img src={recipe.Images[0]} class="object-contain w-full h-full" alt="food" />
							{:else}
								<div class="w-full h-full flex flex-row items-center justify-center text-stone-100">
									<p>No Image</p>
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
					<div
						class="flex flex-col w-96 gap-8 border border-black border-opacity-40 bg-stone-50 p-4 justify-between"
					>
						<div class="flex flex-col w-full place-self-center gap-1">
							<p class="text-2xl">Ingredients</p>
							<hr class="w-full border-0 border-b border-black border-opacity-50" />
							{#each Object.entries(getIngredients(recipe)) as [item, quantity]}
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
		<slot />
	</div>
</dialog>

<style>
	dialog {
		border: none;
		padding: 0;
	}
	dialog::backdrop {
		background: rgba(0, 0, 0, 0.3);
	}
	dialog[open] {
		animation: zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
	}
	@keyframes zoom {
		from {
			transform: scale(0.95);
		}
		to {
			transform: scale(1);
		}
	}
	dialog[open]::backdrop {
		animation: fade 0.2s ease-out;
	}
	@keyframes fade {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
	button {
		display: block;
	}
</style>
