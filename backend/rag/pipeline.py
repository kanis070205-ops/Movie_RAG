from .retriever import retrieve_movies
from .generator import generate_response

def run_rag(query):
    movies = retrieve_movies(query)
    answer = generate_response(query, movies)
    return answer, movies