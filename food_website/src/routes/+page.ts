import type { SearchResult } from '$lib';
/** @type {import('./$types').PageLoad} */
export async function load({ fetch, url }) {
	const res = await fetch('https://34.126.162.255:5000/recommended', {
		credentials: 'include'
	});
	const recommended: SearchResult = await res.json();

	return { recommended };
}
