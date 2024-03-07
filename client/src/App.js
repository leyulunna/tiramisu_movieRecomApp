import React, {useState} from 'react'
import SearchBar from './SearchBar'
import MovieList from './MovieList'
import FavoriteMovies from './FavoriteMovies'
import { Tabs, Tab } from 'react-bootstrap';

const App = () => {
  const [movies, setMovies] = useState([]);
  const [key, setKey] = useState("search");
  const api = 'https://movie-recom-app-3003b9be733c.herokuapp.com';

  const handleSearch = (query) => {
    fetch(api + `/search_movies?query=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(data => {
        setMovies(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const handleAddFavorite = (imdbID) => {
    fetch(api + `/add_to_favorites`, {
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
    <Tabs
      activeKey={key}
      onSelect={(k) => setKey(k)}
      className="mb-3"
    >
      <Tab eventKey="search" title="Search">
        <SearchBar onSearch={handleSearch} />
        <MovieList movies={movies} onAddFavorite={handleAddFavorite} />
      </Tab>
      <Tab eventKey="fav" title="My Favorite List">
        <FavoriteMovies />
      </Tab>
    </Tabs>
  );
}

export default App