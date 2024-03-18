import type { Recipe, SearchResult } from '$lib';
import { page } from '$app/stores';
import type { Folder, FolderResult } from '$lib/elasticsearch.js';
/** @type {import('./$types').PageLoad} */
export const ssr = false;
export async function load({ fetch, url }) {
	const result = (await (await fetch(
		`https://34.126.162.255:5000/folders`,
		{
			credentials: 'include'
		}
	)).json()) as FolderResult
	return { result }
}
