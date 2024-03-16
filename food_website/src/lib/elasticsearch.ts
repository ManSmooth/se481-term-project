export interface SearchResult {
	elapse: number;
	results: Recipe[];
	suggest: string;
	status: string;
}

export interface FolderResult {
	elapse: number
	results: Folder[]
	status: string
	total_hit: number
}


export interface Folder {
	folder_name: string
	index: number
	username: string
	recipes: Recipe[]
}

export interface Recipe {
	rating: number;
	AggregatedRating: number;
	AuthorId: number;
	AuthorName: string;
	Calories: number;
	CarbohydrateContent: number;
	CholesterolContent: number;
	CookTime: string;
	DatePublished: string;
	Description: string;
	FatContent: number;
	FiberContent: number;
	Images: string[];
	Keywords: string[];
	Name: string;
	PrepTime: string;
	ProteinContent: number;
	RecipeCategory: string;
	RecipeId: number;
	RecipeIngredientParts: string[];
	RecipeIngredientQuantities: string[];
	RecipeInstructions: string[];
	RecipeServings: number;
	RecipeYield: string;
	ReviewCount: number;
	SaturatedFatContent: number;
	SodiumContent: number;
	SugarContent: number;
	TotalTime: string;
}

const iso8601DurationRegex =
	/(-)?P(?:([.,\d]+)Y)?(?:([.,\d]+)M)?(?:([.,\d]+)W)?(?:([.,\d]+)D)?T(?:([.,\d]+)H)?(?:([.,\d]+)M)?(?:([.,\d]+)S)?/;
export function parseDuration(iso8601Duration: string) {
	var matches = iso8601Duration.match(iso8601DurationRegex);
	if (matches) {
		return {
			sign: matches[1] === undefined ? '+' : '-',
			years: matches[2] === undefined ? 0 : matches[2],
			months: matches[3] === undefined ? 0 : matches[3],
			weeks: matches[4] === undefined ? 0 : matches[4],
			days: matches[5] === undefined ? 0 : matches[5],
			hours: matches[6] === undefined ? 0 : matches[6],
			minutes: matches[7] === undefined ? 0 : matches[7],
			seconds: matches[8] === undefined ? 0 : matches[8]
		};
	} else return {};
}
