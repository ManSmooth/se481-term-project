import pandas as pd


def create_folder(username: str, folder_name: str, folder_df: pd.DataFrame):
    folder_df = pd.concat(
        [
            folder_df,
            pd.DataFrame(
                [[username, folder_name]], columns=["username", "folder_name"]
            ),
        ],
        ignore_index=True,
    )
    return folder_df


def get_folders_username(username: str, folder_df: pd.DataFrame):
    return folder_df[folder_df["username"] == username].reset_index()


def get_recipes_folder(id: int, bookmark_df: pd.DataFrame, recipes_df: pd.DataFrame):
    return pd.merge(
        bookmark_df[bookmark_df["folder_index"] == id],
        recipes_df,
        how="inner",
        left_on="RecipeId",
        right_on="RecipeId",
    )[["rating"] + list(recipes_df.columns)]


def bookmark_recipe(
    folder_index: int, RecipeID: int, rating: float, bookmark_df: pd.DataFrame
):
    if not bookmark_df[
        (bookmark_df["folder_index"] == folder_index)
        & (bookmark_df["RecipeId"] == RecipeID)
    ].empty:
        bookmark_df.loc[
            (bookmark_df["folder_index"] == folder_index)
            & (bookmark_df["RecipeId"] == RecipeID),
            "rating",
        ] = rating
    else:
        bookmark_df = pd.concat(
            [
                bookmark_df,
                pd.DataFrame(
                    [[folder_index, RecipeID, rating]],
                    columns=["folder_index", "RecipeId", "rating"],
                ),
            ],
            ignore_index=True,
        )
    return bookmark_df
