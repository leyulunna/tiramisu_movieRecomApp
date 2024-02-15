import React, {useState, useEffect} from 'react'

const FavoriteMovies = () => {
  const [favorites, setFavorites] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/movies/favorites')
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

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h2>Favorite Movies</h2>
      <ul>
        {favorites.map(movie => (
          <li key={movie.imdb_id}>
            <h3>{movie.title}</h3>
            <p>Year: {movie.year}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FavoriteMovies