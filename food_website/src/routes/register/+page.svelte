<script lang="ts">
	import { goto } from '$app/navigation';
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import { getUserInformation, type JWTResponse } from '$lib';

	let username = '';
	let display_name = '';
	let password = '';
	const user = getContext('user') as Writable<JWTResponse>;
	function submitForm() {
		fetch('https://34.126.162.255:5000/register', {
			method: 'POST',
			body: JSON.stringify({
				username,
				display_name,
				password
			}),
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		}).then((res) => {
			getUserInformation()
				.then((res) => {
					if (res) {
						user.set(res);
					}
				})
				.catch((err) => {
					goto('/login');
				});
			goto('/');
		});
	}
</script>

<div class="flex flex-row gap-8 justify-center font-serif items-center">
	<form
		class="bg-stone-200 p-8 flex flex-col flex-1 max-w-xl shadow-lg gap-8 font-sans justify-center"
		on:submit|preventDefault={submitForm}
	>
		<div class="flex flex-col gap-2">
			<p class="text-xl">Username</p>
			<input
				type="text"
				class="bg-stone-300 rounded-sm border-b border-black border-opacity-50 px-2 py-1 focus:border-lime-500 focus:bg-stone-200 outline-none transition-all"
				name="username"
				bind:value={username}
			/>
		</div>
		<div class="flex flex-col gap-2">
			<p class="text-xl">Display Name</p>
			<input
				type="text"
				class="bg-stone-300 rounded-sm border-b border-black border-opacity-50 px-2 py-1 focus:border-lime-500 focus:bg-stone-200 outline-none transition-all"
				name="display-name"
				bind:value={display_name}
			/>
		</div>
		<div class="flex flex-col gap-2">
			<p class="text-xl">Password</p>
			<input
				type="password"
				class="bg-stone-300 rounded-sm border-b border-black border-opacity-50 px-2 py-1 focus:border-lime-500 focus:bg-stone-200 outline-none transition-all"
				name="password"
				bind:value={password}
			/>
		</div>
		<div class="flex flex-col gap-2">
			<button
				class="bg-lime-300 w-48 min-w-fit px-4 py-2 place-self-center hover:brightness-75 shadow"
			>
				Register
			</button>
		</div>
	</form>
</div>
