import unittest
import pandas as pd
from food_app.bookmark import (
    create_folder,
    bookmark_recipe,
    get_folders_username,
    get_recipes_folder,
)


class TestBookmarkingFeatures(unittest.TestCase):
    def test_create_folder(self):
        folder_df = pd.DataFrame(
            [
                ["test", "Beef Dishes"],
                ["test", "Asian Dishes"],
                ["test", "Monday Mood"],
            ],
            columns=["username", "folder_name"],
        )
        folder_after_df = create_folder("foo", "bar", folder_df)
        self.assertGreater(len(folder_after_df), len(folder_df))
        self.assertEqual(folder_after_df.tail(1)["username"].values[0], "foo")
        self.assertEqual(folder_after_df.tail(1)["folder_name"].values[0], "bar")

    def test_bookmark(self):
        bookmark_df = pd.DataFrame(
            [[0, 27208, 5.0], [1, 45809, 5.0], [2, 89204, 4.0], [2, 39087, 5.0]],
            columns=["folder_index", "RecipeId", "rating"],
        )
        bookmark_after_df = bookmark_recipe(3, 38, 5.0, bookmark_df)
        self.assertGreater(len(bookmark_after_df), len(bookmark_df))
        self.assertEqual(bookmark_after_df.tail(1)["folder_index"].values[0], 3)
        self.assertEqual(bookmark_after_df.tail(1)["RecipeId"].values[0], 38)
        self.assertEqual(bookmark_after_df.tail(1)["rating"].values[0], 5.0)

    def test_folders_from_username(self):
        folder_df = pd.DataFrame(
            [
                ["test", "Beef Dishes"],
                ["test", "Asian Dishes"],
                ["test", "Monday Mood"],
            ],
            columns=["username", "folder_name"],
        )
        folder_after_df = create_folder("foo", "bar", folder_df)
        self.assertEqual(len(get_folders_username("foo", folder_after_df)), 1)

    def test_get_recipes_folder(self):
        bookmark_df = pd.DataFrame(
            [[0, 1, 5.0], [0, 2, 5.0], [1, 3, 4.0], [1, 4, 5.0]],
            columns=["folder_index", "RecipeId", "rating"],
        )
        recipes_df = pd.DataFrame(
            [[1, "1"], [2, "2"], [3, "3"], [4, "4"]],
            columns=["RecipeId", "Name"],
        )
        result = get_recipes_folder(0, bookmark_df, recipes_df)
        self.assertEqual(result["Name"].values.tolist(), ["1", "2"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
