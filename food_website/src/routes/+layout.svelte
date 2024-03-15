<script lang="ts">
	import '../app.css';
	import { goto, invalidateAll } from '$app/navigation';
	import { onMount, setContext } from 'svelte';
	import { writable } from 'svelte/store';
	let query = '';
	$: search_url = `/search?query=${query}`;
	function handleEnter(event: KeyboardEvent) {
		if (event.key === 'Enter' && event.isTrusted) {
			goto(search_url);
		}
	}
	import type { JWTResponse } from '$lib';
	import { getUserInformation } from '$lib';

	const user = writable<JWTResponse | null>();
	onMount(() => {
		getUserInformation()
			.then((res) => {
				if (res) {
					user.set(res);
				}
			})
			.catch((err) => {
				goto('/login');
			});
	});
	function logout() {
		user.set(null);
		goto('/login');
		localStorage.removeItem('jwt');
	}
	// ...and add it to the context for child components to access
	setContext('user', user);
</script>

<div class="flex justify-start flex-col p-8 gap-8 min-h-[100vh] items-stretch">
	<nav class="flex flex-col items-center justify-between">
		<div class="grid grid-cols-3 bg-stone-200 items-center justify-between w-full">
			<div class="flex flex-row gap-2 items-center">
				<a href="/" class="text-3xl p-4 hover:text-lime-500 font-bold"
					>Recipe<span class="text-lime-500">Me</span></a
				>
				<div class="flex flex-row px-4">
					<a href="/folders" class="hover:text-lime-500 font-bold"
						>Folders</a
					>
				</div>
			</div>
			<div class="flex flex-row gap-2 items-center justify-self-center">
				{#if $user}
					<input
						bind:value={query}
						type="text"
						class="bg-stone-300 rounded-sm border-b-2 border-black border-opacity-50 w-96 px-2 py-1 focus:border-lime-500 focus:bg-stone-200 outline-none transition-all"
						placeholder="Search for recipes"
						on:keypress={handleEnter}
					/>
					<a class="hover:text-lime-500" href="/search?query={query}">Search</a>
				{/if}
			</div>
			<div class="p-4 flex flex-row gap-4 justify-self-end">
				{#if $user}
					<p>Logged in as: <span class="italic">{$user.disp}</span></p>
					<button on:click={logout} class="hover:text-lime-500 font-bold">Logout</button>
				{:else}
					<a href="/login" class="hover:text-lime-500 font-bold">Login</a>
					<a href="/register" class="hover:text-lime-500 font-bold">Register</a>
				{/if}
			</div>
		</div>
		<!-- <img src="/graphic_design_is_my_passion.png" alt="graphics design in my passion (meme)" class="h-64 w-full" /> -->
	</nav>
	<slot />
</div>

<style lang="postcss">
	:global(body) {
		@apply bg-gradient-to-r  from-stone-800 to-stone-700;
	}
</style>
