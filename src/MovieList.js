import React from 'react'
import { FaHeart } from 'react-icons/fa';

const MovieList = ({ movies, onAddFavorite }) => {
  return (
    <div>
      {movies.map((movie) => (
        <div key={movie.imdbID}>
          <h3>{movie.title}</h3>
          <p>{movie.year}</p>
          <button onClick={() => onAddFavorite(movie.imdbID)}>
            <FaHeart /> Add to Favorites
          </button>
        </div>
      ))}
    </div>
  );
}

export default MovieList
