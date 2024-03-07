import React from 'react'
import { FaHeart } from 'react-icons/fa'
import { Button, Card } from 'react-bootstrap'

const MovieList = ({ movies, onAddFavorite }) => {
  return (
    <div>
      <div>
        {movies.map((movie) => (
          <Card key={movie.imdbID} style={{ width: '18rem' }}>
            <Card.Body>
              <Card.Title>{movie.title}</Card.Title>
              <Card.Text>{movie.year}</Card.Text>
              <Button variant="primary" size="sm" onClick={() => onAddFavorite(movie.imdbID)}>
                <FaHeart /> Add to Favorites
              </Button>
            </Card.Body>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default MovieList
