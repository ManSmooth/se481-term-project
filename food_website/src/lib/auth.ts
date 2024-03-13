export interface JWTResponse {
	csrf: string;
	disp: string;
	exp: number;
	fresh: boolean;
	iat: number;
	jti: string;
	nbf: number;
	sub: string;
	type: string;
}

export async function getUserInformation(jwt: string | undefined): Promise<JWTResponse | null> {
	if (!jwt) {
		return null;
	}
	return fetch('http://34.126.162.255:5000/user-detail', {
		headers: {
			Authorization: `Bearer ${jwt}`
		}
	})
		.then(async (res) => {
			const res_json = await res.json();
			return res_json;
		})
		.catch((err) => {
			return null;
		});
}

export interface UserData {
	jwt: string | null;
	user: JWTResponse | null;
}
