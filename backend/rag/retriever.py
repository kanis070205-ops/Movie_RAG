from sentence_transformers import SentenceTransformer
from backend.db.milvus_client import collection
from backend.db.supabase_client import supabase

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_movies(query, top_k=5):

    query_embedding = embed_model.encode(query).tolist()

    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=top_k
    )

    movie_ids = [hit.id for hit in results[0]]

    movies = []

    for movie_id in movie_ids:
        response = supabase.table("movies").select("*").eq("id", movie_id).execute()
        if response.data:
            movies.append(response.data[0])

    return movies