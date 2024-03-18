def get_search_query(query: str):
    return {
        "function_score": {
            "query": {
                "dis_max": {
                    "queries": [
                        {"match": {"Name": query}},
                        {"match": {"RecipeIngredientParts": query}},
                        {"match": {"RecipeInstructions": query}},
                        {"match": {"Keywords": query}},
                    ],
                    "tie_breaker": 0.3,
                }
            },
            "functions": [
                {
                    "script_score": {
                        "script": {
                            "source": "(doc['AggregatedRating'].value * doc['ReviewCount'].value + 4.813715683898263 * 5.316319710056667) / (doc['AggregatedRating'].value + 5.316319710056667)"
                        },
                    },
                    "weight": 1,
                },
                {
                    "script_score": {
                        "script": {"source": "_score"},
                    },
                    "weight": 1,
                },
            ],
            "score_mode": "multiply",
        }
    }


recommend_query = {
    "function_score": {
        "query": {"match_all": {}},
        "functions": [
            {
                "script_score": {
                    "script": {
                        "source": "(doc['AggregatedRating'].value * doc['ReviewCount'].value + 4.813715683898263 * 5.316319710056667) / (doc['AggregatedRating'].value + 5.316319710056667)"
                    },
                },
                "weight": 1,
            },
            {"random_score": {}, "weight": 20},
        ],
        "score_mode": "avg",
    }
}
