import type { Recipe, SearchResult } from '$lib';
import { page } from '$app/stores'
/** @type {import('./$types').PageLoad} */
export async function load({ fetch, url }) {
	const res = await fetch('http://34.126.162.255:5000/recommended');
	const recommended: SearchResult = await res.json();

	return { recommended };
}
