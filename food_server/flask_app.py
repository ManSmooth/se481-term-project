from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
import string
import nltk
import joblib
from elasticsearch import Elasticsearch
import time
import pandas as pd
from scipy import sparse
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    JWTManager,
    set_access_cookies,
)
import lightgbm as lgbm
import numpy as np
import os
from food_app.elastic import get_search_query, recommend_query
from food_app.bookmark import (
    get_folders_username,
    get_recipes_folder,
    bookmark_recipe,
    create_folder,
)
from food_app.recommendation import (
    gen_recommendations,
    recommend_from_folder_index,
    train_model,
)


nltk.download("stopwords")
nltk.download("punkt")

app = Flask(__name__)
app.es_client = Elasticsearch(
    "https://127.0.0.1:9200",
    basic_auth=(
        "elastic",
        "yHcm1Pyq=jnDL_4gw93i",
    ),
    ca_certs="/home/amogus/http_ca.crt",
)
app.recipes_df = pd.read_parquet("/home/amogus/resources/food/recipes.parquet")
app.user_df = pd.read_parquet("/home/amogus/resources/food/user.parquet")
app.folder_df = pd.read_parquet("/home/amogus/resources/food/folder.parquet")
app.bookmark_df = pd.read_parquet("/home/amogus/resources/food/bookmark.parquet")

app.config["JWT_SECRET_KEY"] = "recipeme79"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SAMESITE"] = "None"
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config["CORS_HEADERS"] = "Content-Type"
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:5173"}})
jwt = JWTManager(app)


@app.route("/folder", methods=["POST"])
@cross_origin(origin="localhost", headers=["Content-Type"])
@jwt_required()
def create_folder_request():
    claims = get_jwt()
    folder_name = request.json.get("folder_name", None)
    start = time.time()
    response_object = {"status": "success"}
    app.folder_df = create_folder(claims.get("sub"), folder_name, app.folder_df)
    app.folder_df.to_parquet("/home/amogus/resources/food/folder.parquet")
    train_model(app.bookmark_df)
    end = time.time()
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/bookmark", methods=["POST"])
@cross_origin(origin="localhost", headers=["Content-Type"])
@jwt_required()
def add_bookmark_to_folder():
    folder_index = request.json.get("folder_index", None)
    recipe_id = request.json.get("recipe_id", None)
    rating = request.json.get("rating", None)
    start = time.time()
    response_object = {"status": "success"}
    if folder_index is not None and recipe_id is not None and rating is not None:
        app.bookmark_df = bookmark_recipe(
            folder_index, recipe_id, rating, app.bookmark_df
        )
        app.bookmark_df.to_parquet("/home/amogus/resources/food/bookmark.parquet")
        train_model(app.bookmark_df)
    else:
        response_object["status"] = "fail"
    end = time.time()
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/get_recommendations", methods=["GET"])
@jwt_required()
def recommend_user():
    claims = get_jwt()
    start = time.time()
    response_object = {"status": "success"}
    results = gen_recommendations(
        claims.get("sub"), app.folder_df, app.bookmark_df, app.recipes_df
    )
    end = time.time()
    response_object["results"] = results
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/folder_recommend", methods=["GET"])
@jwt_required()
def recommend_one_folder():
    start = time.time()
    response_object = {"status": "success"}
    argList = request.args.to_dict(flat=False)
    folder_index = argList["folder_index"][0]
    results = recommend_from_folder_index(
        int(folder_index), app.folder_df, app.bookmark_df, app.recipes_df
    )
    end = time.time()
    response_object["total_hit"] = len(results)
    response_object["results"] = (
        results.fillna(np.nan).replace([np.nan], [None]).to_dict("records")
    )
    for i, outt in enumerate(response_object["results"]):
        for k, v in outt.items():
            if isinstance(v, np.ndarray):
                response_object["results"][i][k] = list(v)
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/folder", methods=["GET"])
@jwt_required()
def view_one_folder():
    start = time.time()
    response_object = {"status": "success"}
    argList = request.args.to_dict(flat=False)
    id = argList["id"][0]
    results = get_recipes_folder(int(id), app.bookmark_df, app.recipes_df)
    end = time.time()
    response_object["total_hit"] = len(results)
    response_object["results"] = (
        results.fillna(np.nan).replace([np.nan], [None]).to_dict("records")
    )
    for i, outt in enumerate(response_object["results"]):
        for k, v in outt.items():
            if isinstance(v, np.ndarray):
                response_object["results"][i][k] = list(v)
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/folders", methods=["GET"])
@jwt_required()
def view_all_folders():
    start = time.time()
    claims = get_jwt()
    response_object = {"status": "success"}
    folders = get_folders_username(claims.get("sub"), app.folder_df).to_dict(
        orient="records"
    )
    for folder in folders:
        recipes = (
            get_recipes_folder(folder["index"], app.bookmark_df, app.recipes_df)
            .fillna(np.nan)
            .replace([np.nan], [None])
            .sort_values("rating", ascending=False)
            .to_dict(orient="records")
        )
        for i, outt in enumerate(recipes):
            for k, v in outt.items():
                if isinstance(v, np.ndarray):
                    recipes[i][k] = list(v)
        folder["recipes"] = recipes
    end = time.time()
    response_object["total_hit"] = len(folders)
    response_object["results"] = folders
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/user-detail", methods=["GET"])
@jwt_required()
def get_jwt_data():
    claims = get_jwt()
    return make_response(jsonify(dict(claims)), 200)


@app.route("/login", methods=["POST"])
@cross_origin(origin="localhost", headers=["Content-Type"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    try:
        user = (
            app.user_df.reset_index()[
                (app.user_df["username"] == username)
                & (app.user_df["password"] == password)
            ]
            .iloc[0]
            .to_dict()
        )
        print(user)
        additional_claims = {"disp": user.get("display_name")}
        access_token = create_access_token(
            identity=user.get("username"), additional_claims=additional_claims
        )
        resp = make_response(jsonify({}), 200)
        set_access_cookies(resp, access_token)
        return resp
    except IndexError:
        return make_response(jsonify({"msg": "Bad username or password"}), 401)


@app.route("/register", methods=["POST"])
@cross_origin(origin="localhost", headers=["Content-Type"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    display_name = request.json.get("display_name", None)

    if app.user_df[(app.user_df["username"] == "username")].shape[0] > 0:
        return make_response(jsonify({"msg": "Bad username"}), 401)
    else:
        app.user_df = pd.concat(
            [
                app.user_df,
                pd.DataFrame(
                    [[username, password, display_name]],
                    columns=["username", "password", "display_name"],
                ),
            ],
            ignore_index=True,
        )
        app.user_df.to_parquet("/home/amogus/resources/food/user.parquet")
        additional_claims = {"disp": display_name}
        access_token = create_access_token(
            identity=username, additional_claims=additional_claims
        )
        resp = make_response(jsonify({}), 200)
        set_access_cookies(resp, access_token)
        return resp


@app.route("/recommended", methods=["GET"])
@jwt_required()
def get_recommended():
    start = time.time()
    response_object = {"status": "success"}
    results = app.es_client.search(
        index="recipes",
        size=6,
        query=recommend_query,
    )
    end = time.time()
    total_hit = results["hits"]["total"]["value"]
    results_df = pd.DataFrame(
        [[hit["_score"], *hit["_source"].values()] for hit in results["hits"]["hits"]],
        columns=["score"] + list(results["hits"]["hits"][0]["_source"].keys()),
    )
    response_object["total_hit"] = total_hit
    response_object["results"] = results_df.to_dict("records")
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/search", methods=["GET"])
@jwt_required()
def search():
    start = time.time()
    response_object = {"status": "success"}
    argList = request.args.to_dict(flat=False)
    query = argList["query"][0]
    results = app.es_client.search(
        index="recipes",
        size=12,
        query=get_search_query(query),
    )
    end = time.time()
    total_hit = results["hits"]["total"]["value"]
    if len(results["hits"]["hits"]) > 0:
        results_df = pd.DataFrame(
            [
                [hit["_score"], *hit["_source"].values()]
                for hit in results["hits"]["hits"]
            ],
            columns=["score"] + list(results["hits"]["hits"][0]["_source"].keys()),
        )
    else:
        results_df = pd.DataFrame()
    response_object["total_hit"] = total_hit
    response_object["results"] = results_df.to_dict("records")
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/recipes/<int:id>", methods=["GET"])
@jwt_required()
def get_by_id(id: int):
    start = time.time()
    response_object = {"status": "success"}
    result = app.es_client.get(index="recipes", id=id)
    end = time.time()
    result_df = pd.DataFrame(
        [[*result["_source"].values()]],
        columns=list(result["_source"].keys()),
    )
    response_object["results"] = result_df.to_dict("records")
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.route("/suggest", methods=["GET"])
@jwt_required()
def suggest():
    start = time.time()
    response_object = {"status": "success"}
    argList = request.args.to_dict(flat=False)
    query = argList["query"][0]
    query_dictionary = {
        "suggest": {
            "text": query,
            "suggest-1": {"term": {"field": "all_texts"}},
            "suggest-2": {"term": {"field": "Name"}},
            "suggest-3": {"term": {"field": "Description"}},
            "suggest-4": {"term": {"field": "RecipeInstructions"}},
        }
    }
    res = app.es_client.search(index="recipes", body=query_dictionary)

    p = []
    for term in np.array(list(res["suggest"].values())).T:
        result = {}
        result["text"] = term[0]["text"]
        options = [v["options"] for v in term]
        result["candidates"] = {}
        for option in options:
            candidates = {}
            if len(option) > 0:
                candidates["text"] = option[0]["text"]
                for candidate in option:
                    if candidate["text"] not in result["candidates"]:
                        result["candidates"][candidate["text"]] = {
                            "score": candidate["score"],
                            "freq": candidate["freq"],
                        }
                    else:
                        result["candidates"][candidate["text"]]["score"] = (
                            result["candidates"][candidate["text"]]["score"]
                            * result["candidates"][candidate["text"]]["freq"]
                            + candidate["score"] * candidate["freq"]
                        ) / (
                            result["candidates"][candidate["text"]]["freq"]
                            + candidate["freq"]
                        )
                        result["candidates"][candidate["text"]]["freq"] = (
                            result["candidates"][candidate["text"]]["freq"]
                            + candidate["freq"]
                        )
        p += [result["candidates"]]
    out = [""] * len(query.split())
    for i, pp in enumerate(p):
        if pp:
            df = pd.DataFrame.from_dict(pp, orient="index")
            R = (df["score"] * df["freq"]).sum() / df["freq"].sum()
            W = df["freq"].mean()
            df["bayes_score"] = (df["score"] * df["freq"] + W * R) / (df["freq"] + W)
            out[i] = df.sort_values("bayes_score", ascending=False).head(1).index[0]
        else:
            out[i] = query.split()[i]
    " ".join(out)
    end = time.time()
    response_object["suggest"] = " ".join(out)
    response_object["elapse"] = end - start
    return make_response(response_object, 200)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Headers"] = (
        "Origin, X-Requested-With, Content-Type, Accept"
    )
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", ssl_context="adhoc")
