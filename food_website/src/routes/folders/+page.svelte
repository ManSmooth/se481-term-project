<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import type { Folder } from '$lib/elasticsearch';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import FolderSection from './folder_section.svelte';
	/** @type {import('./$types').PageData} */
	export let data: any;
	let showCreateFolder: boolean = false;
	let folderName = '';
	$: folders = data.result.results as Folder[];
	function submitForm() {
		fetch('https://34.126.162.255:5000/folder', {
			method: 'POST',
			body: JSON.stringify({
				folder_name: folderName
			}),
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include'
		}).then((res) => {
			invalidateAll();
		});
	}
	onMount(() => {
		if (!('results' in data.result)) {
			goto('/login');
		}
	});
</script>

<div class="flex flex-row gap-8 justify-center font-serif items-center">
	<div class="flex flex-col gap-8 w-full items-center">
		<p class="text-3xl font-bold text-stone-100 px-4 py-2 border-4 border-stone-100 rounded-md">
			Folders
		</p>
		{#each folders || [] as folder}
			<FolderSection bind:folder bind:folders></FolderSection>
		{/each}
		<div class="flex flex-col gap-4 items-center">
			<button
				class="font-sans bg-lime-400 px-2 py-1 rounded-md border border-stone-900 border-opacity-30 w-fit"
				on:click={() => (showCreateFolder = !showCreateFolder)}>Create new Folder</button
			>
			{#if showCreateFolder}
				<form
					class="transition-all border border-stone-900 rounded-lg border-opacity-30 p-4 flex flex-col gap-4 w-fit bg-stone-100"
					on:submit|preventDefault={submitForm}
				>
					<div class="flex flex-row gap-2 items-center">
						<label for="folder_name">Folder Name</label>
						<input
							type="text"
							class="bg-stone-300 rounded-sm border-b border-black border-opacity-50 px-2 py-1 focus:border-lime-500 focus:bg-stone-200 outline-none transition-all w-96"
							name="folder_name"
							bind:value={folderName}
						/>
					</div>
					<button
						class="font-sans bg-yellow-400 px-2 py-1 rounded-md border border-stone-900 border-opacity-30 w-fit disabled:saturate-0"
						disabled={!folderName}>Confirm</button
					>
				</form>
			{/if}
		</div>
	</div>
</div>
