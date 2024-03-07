import React, {useState, useEffect} from 'react'
import { FaUserEdit, FaTrash, FaSync } from 'react-icons/fa'
import { Button, Card } from 'react-bootstrap'
import './FavoritesMovie.css'

const FavoriteMovies = () => {
  const [favorites, setFavorites] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const api = 'https://movie-recom-app-3003b9be733c.herokuapp.com';

  useEffect(() => {
    fetch(api + '/movies/favorites')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch.');
        }
        return response.json();
      })
      .then(data => {
        setFavorites(data);
        setIsLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setIsLoading(false);
      });
  }, []);

  const handleRemoveFavorite = (imdbID) => {
    fetch(api + `/movies/favorite/` + imdbID, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Update your state based on the response
      setFavorites(currentFavorites => currentFavorites.filter(movie => movie.imdbID !== imdbID));
      console.log('Favorite deleted:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  const refreshFavorites = () => {
    setIsLoading(true);
    fetch(api + '/movies/favorites')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch.');
        }
        return response.json();
      })
      .then(data => {
        setFavorites(data);
        setIsLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setIsLoading(false);
      });
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <div className='header'>
        <h2>Favorite Movies</h2>
        <Button variant="primary" size="sm" onClick={() => refreshFavorites()}>
          <FaSync /> Refresh
        </Button>
      </div>
      <ul>
        {favorites.map(movie => (
          <Card key={movie.imdb_id} style={{ width: '18rem' }}>
          <Card.Body>
            <Card.Title>{movie.title}</Card.Title>
            <Card.Text>Year:  {movie.year}</Card.Text>
            <Button variant="primary" size="sm">
              <FaUserEdit /> Edit
            </Button>
            <Button variant="danger" size="sm" onClick={() => handleRemoveFavorite(movie.imdb_id)}>
              <FaTrash /> Delete
            </Button>
          </Card.Body>
        </Card>
        ))}
      </ul>
    </div>
  );
}

export default FavoriteMovies
