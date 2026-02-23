
from fastapi import FastAPI
from pydantic import BaseModel
from .rag.pipeline import run_rag
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
print("APP STARTING...")
# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    description: str

@app.post("/api/search")
async def search_movies(request: SearchRequest):
    answer, movies = run_rag(request.description)
    # Return detailed movie info from Postgres and Groq LLM output
    movie_details = []
    import json
    for m in movies:
        # Parse genres and keywords if they are JSON strings
        genres = m.get("genres", "")
        if isinstance(genres, str):
            try:
                genres = ", ".join([g["name"] for g in json.loads(genres)])
            except Exception:
                pass
        keywords = m.get("keywords", "")
        if isinstance(keywords, str):
            try:
                keywords = ", ".join([k["name"] for k in json.loads(keywords)])
            except Exception:
                pass
        movie_details.append({
            "title": m.get("title"),
            "vote_average": m.get("vote_average"),
            "release_date": m.get("release_date"),
            "tagline": m.get("tagline"),
            "overview": m.get("overview"),
            "genres": genres,
            "keywords": keywords,
        })
    return {
        "llm_output": answer,
        "movies": movie_details
    }
