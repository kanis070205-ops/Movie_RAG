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
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ error: 'Failed to fetch movie info. Please try again.' });
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1 className="fancy-title">🎬 CineRAG: Discover Your Movie Magic!</h1>
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
              <h2 className="movie-name">{result.title || 'Movie Title'}</h2>
              <p className="movie-desc">{result.description || 'No description found.'}</p>
              <div className="movie-meta">
                <span>⭐ Rating: {result.rating || 'N/A'}</span>
                <span>🎭 Genre: {result.genre || 'N/A'}</span>
                <span>📅 Year: {result.year || 'N/A'}</span>
              </div>
              <div className="llm-response">
                <strong>AI Insight:</strong>
                <p>{result.llm_response ? result.llm_response : 'No AI response. Please check backend integration.'}</p>
              </div>
            </>
          )}
        </div>
      )}
      <footer className="fancy-footer">
        <span>✨ Powered by Milvus, Postgres & LLM ✨</span>
      </footer>
    </div>
  );
}

export default App;
