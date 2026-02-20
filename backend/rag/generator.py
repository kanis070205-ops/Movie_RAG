
import os
import requests


def generate_response(query, movies):

    context = ""

    for i, movie in enumerate(movies, 1):
        context += f"""
Movie {i}:
Title: {movie['title']}
Overview: {movie['overview']}
Rating: {movie.get('vote_average', 'N/A')}
"""

    prompt = f"""
STRICT RULES:
- Only recommend from the provided movies.
- Do not invent new ones.

User request:
{query}

Available movies:
{context}

Recommend and explain.
"""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]