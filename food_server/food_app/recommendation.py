import pandas as pd
from scipy import sparse
import joblib
import os
import lightgbm as lgbm
import numpy as np


def get_keywords_df():
    return pd.DataFrame.sparse.from_spmatrix(
        sparse.load_npz("/home/amogus/resources/food/keywords_df.npz"),
        columns=joblib.load("/home/amogus/resources/food/keywords_df_columns.joblib"),
    )


def train_model(bookmark_df: pd.DataFrame):
    feature_columns = recipes_numerical.columns.delete(0)
    folders_recipes_df = pd.merge(
        bookmark_df.sort_values(["folder_index", "rating"]),
        recipes_numerical,
        how="inner",
        left_on="RecipeId",
        right_on="RecipeId",
    )
    target_column = ["rating"]
    groups = folders_recipes_df["folder_index"].value_counts().sort_index().to_list()
    ranker.fit(
        folders_recipes_df[feature_columns],
        folders_recipes_df[target_column],
        group=groups,
    )
    joblib.dump(ranker, "/home/amogus/resources/food/ranker.joblib")


def recommend_from_folder_index(
    index: int,
    folder_df: pd.DataFrame,
    bookmark_df: pd.DataFrame,
    recipes_df: pd.DataFrame,
):
    folder_keywords = np.unique(
        pd.merge(
            bookmark_df[bookmark_df["folder_index"] == index],
            recipes_df,
            how="inner",
            left_on="RecipeId",
            right_on="RecipeId",
        )["Keywords"].explode()
    )
    exclude_kw = list(set(keywords_df.columns).difference(folder_keywords))
    pred_df = recipes_numerical[recipes_numerical[exclude_kw].values.sum(axis=1) == 0]
    preds = ranker.predict(pred_df[recipes_numerical.columns.delete(0)])
    return recipes_df.iloc[
        pd.concat(
            [pred_df.reset_index(), pd.Series(preds).to_frame("rank_score")], axis=1
        )
        .sort_values("rank_score", ascending=False)
        .head(9)
        .sample(frac=1)
        .head(6)
        .set_index("index")
        .index
    ]


def recommend_from_user(
    user: str,
    folder_df: pd.DataFrame,
    bookmark_df: pd.DataFrame,
    recipes_df: pd.DataFrame,
):
    folder_keywords = np.unique(
        pd.merge(
            bookmark_df[
                bookmark_df["folder_index"].isin(
                    folder_df[folder_df["username"] == user].index
                )
            ],
            recipes_df,
            how="inner",
            left_on="RecipeId",
            right_on="RecipeId",
        )["Keywords"].explode()
    )
    exclude_kw = list(set(keywords_df.columns).difference(folder_keywords))
    pred_df = recipes_numerical[recipes_numerical[exclude_kw].values.sum(axis=1) == 0]
    preds = ranker.predict(pred_df[recipes_numerical.columns.delete(0)])
    return recipes_df.iloc[
        pd.concat(
            [pred_df.reset_index(), pd.Series(preds).to_frame("rank_score")], axis=1
        )
        .sort_values("rank_score", ascending=False)
        .head(9)
        .sample(frac=1)
        .head(6)
        .set_index("index")
        .index
    ]


def gen_recommendations(
    user: str,
    folder_df: pd.DataFrame,
    bookmark_df: pd.DataFrame,
    recipes_df: pd.DataFrame,
):
    recommend_result = dict()
    if not folder_df[folder_df["username"] == user].empty:
        if pd.merge(
            folder_df[folder_df["username"] == user],
            bookmark_df,
            left_index=True,
            right_on="folder_index",
            how="inner",
        ).empty:
            recommend_result["recommend_from_summary"] = {"results": []}
        else:
            recommend_result["recommend_from_summary"] = {
                "results": recommend_from_user(user, folder_df, bookmark_df, recipes_df)
                .fillna(np.nan)
                .replace([np.nan], [None])
                .to_dict(orient="records")
            }
            for i, outt in enumerate(
                recommend_result["recommend_from_summary"]["results"]
            ):
                for k, v in outt.items():
                    if isinstance(v, np.ndarray):
                        recommend_result["recommend_from_summary"]["results"][i][k] = (
                            list(v)
                        )
        folder = folder_df[folder_df["username"] == user].sample(frac=1).head(1)
        if pd.merge(
            folder,
            bookmark_df,
            left_index=True,
            right_on="folder_index",
            how="inner",
        ).empty:
            recommend_result["recommend_from_folder"] = {
                "folder_name": folder.iloc[0]["folder_name"],
                "results": [],
            }
        else:
            recommend_result["recommend_from_folder"] = {
                "folder_name": folder.iloc[0]["folder_name"],
                "results": recommend_from_folder_index(
                    folder.index[0], folder_df, bookmark_df, recipes_df
                )
                .fillna(np.nan)
                .replace([np.nan], [None])
                .to_dict(orient="records"),
            }
            for i, outt in enumerate(
                recommend_result["recommend_from_folder"]["results"]
            ):
                for k, v in outt.items():
                    if isinstance(v, np.ndarray):
                        recommend_result["recommend_from_folder"]["results"][i][k] = (
                            list(v)
                        )
        recommend_result["recommend_from_random"] = {
            "results": recipes_df.sample(6)
            .fillna(np.nan)
            .replace([np.nan], [None])
            .to_dict(orient="records")
        }
        for i, outt in enumerate(recommend_result["recommend_from_random"]["results"]):
            for k, v in outt.items():
                if isinstance(v, np.ndarray):
                    recommend_result["recommend_from_random"]["results"][i][k] = list(v)
    return recommend_result


ranker = None
if os.path.isfile("/home/amogus/resources/food/ranker.joblib"):
    ranker = joblib.load("/home/amogus/resources/food/ranker.joblib")
else:
    ranker = lgbm.LGBMRanker(
        min_child_samples=1,
        num_leaves=63,
        learning_rate=0.01,
        n_estimators=1000,
        verbosity=-1,
    )
    train_model(pd.read_parquet("/home/amogus/resources/food/bookmark.parquet"))
keywords_df = get_keywords_df()
keywords_df = get_keywords_df()
recipes_numerical = pd.merge(
    pd.read_parquet("/home/amogus/resources/food/recipes.parquet")[
        ["RecipeId", "AggregatedRating", "ReviewCount"]
    ].fillna(0.0),
    keywords_df,
    left_index=True,
    right_index=True,
)
