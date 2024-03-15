
/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch, url }) {
	process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"
}
