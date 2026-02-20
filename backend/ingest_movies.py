import os
import json
import time
from dotenv import load_dotenv
from supabase import create_client
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZILLIZ_URI = os.getenv("ZILLIZ_URI")
ZILLIZ_TOKEN = os.getenv("ZILLIZ_TOKEN")

# Connect Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Connect Milvus
connections.connect(
    alias="default",
    uri=ZILLIZ_URI,
    token=ZILLIZ_TOKEN
)

collection = Collection("movies")

# Load embedding model (FREE local)
model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_names(json_string):
    try:
        items = json.loads(json_string)
        return ", ".join([item["name"] for item in items])
    except:
        return ""


def generate_embedding(text):
    return model.encode(text).tolist()


def fetch_movies(limit=10000):
    response = supabase.table("movies").select("*").limit(limit).execute()
    return response.data


def ingest_movies():
    movies = fetch_movies()
    print(f"Fetched {len(movies)} movies")

    batch_ids = []
    batch_embeddings = []
    batch_size = 100

    for movie in movies:

        if not movie.get("overview"):
            continue

        genres_text = extract_names(movie.get("genres", "[]"))
        keywords_text = extract_names(movie.get("keywords", "[]"))

        text = f"""
        Title: {movie.get('title', '')}
        Overview: {movie.get('overview', '')}
        Genres: {genres_text}
        Keywords: {keywords_text}
        """

        embedding = generate_embedding(text)

        batch_ids.append(int(movie["id"]))
        batch_embeddings.append(embedding)

        if len(batch_ids) >= batch_size:
            collection.insert([batch_ids, batch_embeddings])
            print(f"Inserted batch of {len(batch_ids)}")
            batch_ids = []
            batch_embeddings = []

    if batch_ids:
        collection.insert([batch_ids, batch_embeddings])
        print(f"Inserted final batch of {len(batch_ids)}")

    print("✅ All embeddings stored successfully!")


if __name__ == "__main__":
    ingest_movies()