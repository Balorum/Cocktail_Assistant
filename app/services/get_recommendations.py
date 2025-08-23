from database.embedding_db import PC_INDEX
from services.gemini_llm import check_filters, extract_preferences
import json


def apply_filters(user_query):
    applied_filters = check_filters(user_query)
    filter_list = []
    for key, value in applied_filters.items():
        if value is not None:
            filter = {}
            if isinstance(value, list):
                for i in value:
                    filter[key] = {"$in": value}
            else:
                filter[key] = value
            filter_list.append(filter)
    if len(filter_list) > 1:
        final_filter = {"$and": filter_list}
    elif len(filter_list) == 1:
        final_filter = filter_list[0]
    else:
        final_filter = None
    print(final_filter)
    return final_filter


def apply_user_preferences(user_query, user_id):
    # with open("data/processed/ingredients_synonyms.json", "r", encoding="utf-8") as f:
    #     synonyms_dict = json.load(f)
    preferences = extract_preferences(user_query)
    profile_text = f"User likes {', '.join(preferences['love_ingredients'])}, " \
                   f"dislikes {', '.join(preferences['hate_ingredients'])}, " \
                   f"favorite cocktails: {', '.join(preferences['love_cocktails'])}"
    pinecone_record = {"_id": f"{user_id}",
                       "text": profile_text,}
    for key, value in preferences.items():
        if not value:
            pinecone_record[key] = value
    PC_INDEX.upsert_records("user-cocktail-preferences",
        [
            pinecone_record
        ]
        )
    return preferences


def get_pinecode_query(user_query, top_k=5, filters=None):
    query = {
        "inputs": {"text": user_query},
        "top_k": top_k
    }
    if filters:
        query["filter"] = filters
    return query


def get_recommendations(user_query, user_id, top_k=5):

    applied_preferences = apply_user_preferences(user_query, user_id)
    applied_filters = apply_filters(user_query)
    query = get_pinecode_query(user_query, top_k, applied_filters)

    results = PC_INDEX.search(
        namespace="cocktails-embeddings-namespace",
        query=query,
        fields=["name", "text", "ingredients", "instructions", "glassType", "alcoholic", "category"]
    )
    return results
