import type { Recipe, SearchResult } from '$lib';

/** @type {import('./$types').PageLoad} */
export async function load({ fetch, params }) {
	const res = await fetch(`https://34.126.162.255:5000/recipes/${params.id}`, {
		credentials: 'include'
	});
	const result: SearchResult = await res.json();
	const recipe: Recipe = result.results[0];

	return { recipe };
}
