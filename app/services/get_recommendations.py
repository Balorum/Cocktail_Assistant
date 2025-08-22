from database.embedding_db import PC_INDEX
from services.gemini_llm import check_filters


def get_recommendations(user_query, top_k=5):


    # Add category to pinecode
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


    results = PC_INDEX.search(
        namespace="cocktails-embeddings-namespace",
        query={
            "inputs": {"text": user_query},
            "top_k": top_k,
            "filter": final_filter if len(filter_list) > 0 else None
        },
        fields=["name", "text", "ingredients", "instructions", "glassType", "alcoholic", "category"]
    )
    return results
