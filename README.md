# Movie Favorites App

## Introduction (Written by YenChen)
- This Python application provides functionality to manage a user's favorite movies. 
- Users can utilize this application to search for movies in the IMDB database, save their favorite movies to a "My Favorites" list, add movies to their favorites, view their favorite movies, and remove movies from their favorites.
- The application uses Flask as the web framework and SQLAlchemy to interact with a database.

## Installation (Written by YenChen)

1. Clone the repository:
```bash
git clone https://github.com/leyulunna/tiramisu_movieRecomApp.git
```

2. Install dependencies:
```bash
pipenv install
```

3. Set up the database:
- Open a Python shell
- Inside the Python shell, run the following commands:
```bash
from app import db
db.create_all()
exit()
```

## Features (Written by YenChen)
1. User can view all favorite movies(work with YuLun):
- Allows users to see a comprehensive list of all their favorite movies.
- Endpoint: Send a GET request to /movies/favorites.

2. User can view the create-new-favorite-movie page:
- Allows users to see the create-new-favorite-movie page.
- Endpoint: Send a GET request to /movies/favorite/new.

3. User can create a new movie to the favorites:
- Permits users to create a new movie to their favorites list by providing details in JSON format.
- Endpoint: Send a POST request to /movies/favorite/new with the movie details in JSON format.

4. User can view details of a specific movie in their favorites:
- Allows users to retrieve detailed information about a specific movie.
- Endpoint: Send a GET request to /movies/favorite/<imdb_id>, replacing <imdb_id> with the IMDb ID of the movie.

5. User can remove a specific movie in their favorites:
- Enables users to remove a specific movie from the system entirely.
- Endpoint: Use a DELETE request to /movies/favorite/<imdb_id>.

6. User can retrieve details for editing a specific movie in their favorites:
- Provides users with detailed information about a movie for the purpose of editing.
- Endpoint: Send a GET request to /movies/favorite/<imdb_id>/edit, replacing <imdb_id> with the IMDb ID of the movie.

7. User can update the details of a specific movie in their favorites:
- Allows users to update the details of a specific movie using a JSON PUT request.
- Endpoint: Send a JSON PUT request to /movies/favorite/<imdb_id>, replacing <imdb_id> with the IMDb ID of the movie.
