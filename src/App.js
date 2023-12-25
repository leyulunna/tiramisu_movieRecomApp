import React, {useState} from 'react'
import SearchBar from './SearchBar'
import MovieList from './MovieList'
import FavoriteMovies from './FavoriteMovies'

const App = () => {
  const [movies, setMovies] = useState([]);
  const [showFavorites, setShowFavorites] = useState(false);

  const handleSearch = (query) => {
    fetch(`http://127.0.0.1:5000/search_movies?query=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        setMovies(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const toggleShowFavorites = () => {
    setShowFavorites(!showFavorites);
  };

  const handleAddFavorite = (imdbID) => {
    fetch(`http://127.0.0.1:5000/add_to_favorites`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ imdb_id: imdbID }) // Ensure the key matches what your backend expects
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Update your state based on the response
      // This depends on how your backend handles the add to favorites request
      console.log('Favorite added:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  return (
    <div>
      <div>
        <button onClick={toggleShowFavorites}>
          {showFavorites ? "Show Search Results" : "Show Favorite Movies"}
        </button>
      </div>
      <div>
        <SearchBar onSearch={handleSearch} />
        {showFavorites ? <FavoriteMovies /> : <MovieList movies={movies} onAddFavorite={handleAddFavorite} />}
      </div>
    </div>
  );
}

export default App
