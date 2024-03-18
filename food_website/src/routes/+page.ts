import type { FolderResult, RecommendResult, SearchResult } from '$lib/elasticsearch.js';
/** @type {import('./$types').PageLoad} */
export const ssr = false;
export async function load({ fetch, url }) {
	const other_res = await fetch('https://34.126.162.255:5000/recommended', {
		credentials: 'include'
	});
	const folder_result = (await (await fetch(
		`https://34.126.162.255:5000/folders`,
		{
			credentials: 'include'
		}
	)).json()) as FolderResult
	const other_recommend: SearchResult = await other_res.json();

	return { other_recommend, folder_result };
}
