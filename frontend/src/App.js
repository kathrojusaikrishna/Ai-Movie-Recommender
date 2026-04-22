import { useState } from "react";
import "./App.css";

function App() {
  const [movie, setMovie] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const getRecommendations = async () => {
    if (!movie) return;

    setLoading(true);

    try {
      const res = await fetch(`http://127.0.0.1:5000/recommend?movie=${movie}`);
      const data = await res.json();

      if (data[0] === "Movie not found") {
        alert("Movie not found!");
        setResults([]);
      } else {
        setResults(data);
      }
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>🎬 AI Movie Recommender</h1>

      <div className="search-box">
        <input
          type="text"
          placeholder="Enter movie name (e.g., Avatar)"
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
        />

        <button onClick={getRecommendations}>
          {loading ? "Loading..." : "Recommend"}
        </button>
      </div>

      <div className="results">
        {results.map((m, i) => (
          <div key={i} className="movie-card">
            <img
              src={
                m.poster || "https://via.placeholder.com/300x450?text=No+Image"
              }
              alt={m.title}
            />
            <p>{m.title}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
