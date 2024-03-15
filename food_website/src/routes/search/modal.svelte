<script lang="ts">
	export let index: number = 0; // boolean
	export let currentIndex: number = -1;

	let dialog: HTMLDialogElement; // HTMLDialogElement

	$: if (dialog && (index === currentIndex)) dialog.showModal();
</script>

<!-- svelte-ignore a11y-click-events-have-key-events a11y-no-noninteractive-element-interactions -->
<dialog
	bind:this={dialog}
	on:close={() => (currentIndex = -1)}
	on:click|self={() => dialog.close()}
	class="max-w-full p-0"
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div on:click|stopPropagation>
		<button class="absolute top-4 right-4 bg-lime-300 px-2 py-1 border border-black" on:click={() => dialog.close()}>Close</button>
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
