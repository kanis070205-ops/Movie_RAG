import streamlit as st
from rag.pipeline import run_rag

st.title("🎬 AI Movie Recommendation")

query = st.text_input("Describe the movie you want")

if st.button("Search"):
    if query:
        with st.spinner("Thinking..."):
            answer, movies = run_rag(query)

        st.write(answer)

        with st.expander("Retrieved Movies"):
            for m in movies:
                st.write(m["title"])