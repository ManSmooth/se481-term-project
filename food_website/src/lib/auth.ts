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

export async function getUserInformation(): Promise<JWTResponse | null> {
	return fetch('https://34.126.162.255:5000/user-detail', {
		credentials: 'include'
	})
		.then(async (res) => {
			const res_json = await res.json();
			return res_json;
		})
		.catch((err) => {
			return Promise.reject(err);
		});
}

export interface UserData {
	jwt: string | null;
	user: JWTResponse | null;
}
