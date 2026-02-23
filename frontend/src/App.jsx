import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      // Replace with your backend endpoint
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: query }),
      });
      const data = await response.json();
      // Adapt to backend response: { llm_output, movies }
      setResult({
        llm_output: data.llm_output,
        movies: data.movies
      });
    } catch (error) {
      setResult({ error: 'Failed to fetch movie info. Please try again.' });
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1 className="fancy-title">🎬 CineRAG: Discover Your Movie !</h1>
      <form className="movie-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Ask about any movie..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          className="movie-input"
          required
        />
        <button className="movie-btn" disabled={loading}>
          {loading ? 'Searching...' : 'Find Movie'}
        </button>
      </form>
      {/* No intro section, keep minimal look */}
      {loading && (
        <div style={{marginTop: '2rem'}}>
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" className="spin">
            <circle cx="24" cy="24" r="20" stroke="#ffd700" strokeWidth="4" strokeDasharray="80" strokeDashoffset="60" />
          </svg>
          <div style={{color:'#ffd700',marginTop:'1rem',fontWeight:'bold'}}>Fetching cinematic wisdom...</div>
        </div>
      )}
      {result && !loading && (
        <div className="movie-result">
          {result.error ? (
            <div className="error">{result.error}</div>
          ) : (
            <>
              <div className="llm-response">
                <strong>AI Insight:</strong>
                <p>{result.llm_output ? result.llm_output : 'No AI response. Please check backend integration.'}</p>
              </div>
              {result.movies && result.movies.length > 0 && (
                <div className="movie-list-grid">
                  {result.movies.map((movie, idx) => (
                    <div key={idx} className="movie-card">
                      <div className="movie-card-header">
                        <h3>{movie.title}</h3>
                        <span className="movie-rating">⭐ {movie.vote_average || 'N/A'}</span>
                      </div>
                      <div className="movie-meta-row">
                        <span className="movie-genre">🎭 {movie.genres || 'N/A'}</span>
                        <span className="movie-date">📅 {movie.release_date || 'N/A'}</span>
                      </div>
                      {movie.tagline && <div className="movie-tagline">“{movie.tagline}”</div>}
                      <div className="movie-overview">{movie.overview}</div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      )}

    </div>
  );
}

export default App;
