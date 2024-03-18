import type { Recipe, SearchResult } from '$lib';
import { page } from '$app/stores';
import type { FolderResult } from '$lib/elasticsearch.js';
/** @type {import('./$types').PageLoad} */
export async function load({ fetch, url }) {
	const res = await fetch(
		`https://34.126.162.255:5000/search?query=${url.searchParams.get('query')}`,
		{
			credentials: 'include'
		}
	);
	const result: SearchResult = await res.json();
	const suggest_res = await fetch(
		`https://34.126.162.255:5000/suggest?query=${url.searchParams.get('query')}`,
		{
			credentials: 'include'
		}
	);
	const suggest_result: SearchResult = await suggest_res.json();
	const folder_result = (await (await fetch(
		`https://34.126.162.255:5000/folders`,
		{
			credentials: 'include'
		}
	)).json()) as FolderResult

	return { result, suggest_result, query: url.searchParams.get('query'), folder_result };
}
