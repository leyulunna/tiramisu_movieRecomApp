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
- Choose one of the following options:
### Option 1: For regular dependencies
```bash
pipenv install
```
### Option 2: For both regular and development dependencies
```bash
pipenv install --dev
```

3. Set up the database:
- Open a Python shell
- Inside the Python shell, run the following commands:
```bash
from app import db
db.create_all()
exit()
```

4. Running the Application
- To run the application, use one of the following commands:
```bash
python3 -m pipenv shell
pip install flask-cors
pip install requests
export FLASK_APP=flask-server.api
flask run
```

## Features (Written by YenChen)
1. User can view all favorite movies(work with YuLun):
- Allows users to see a comprehensive list of all their favorite movies.
- Endpoint: Send a GET request to /movies/favorites.
![Imgur](https://i.imgur.com/Krms6aj.png)

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

8. User can search movies from The Open Movie Database by inputting keywords on the search bar:
- Endpoint: Send a JSON GET request to /search_movies?query=<query>, keywords inputted by users.
![Imgur](https://i.imgur.com/zfKpALO.png)

9. User can add movies from the search results directly to their favorites page.
- Endpoint: Send a JSON POST request to /add_to_favorites, the payload is {"imdb_id": "<imdb_id>"}
![Imgur](https://i.imgur.com/9rYgqYz.png)