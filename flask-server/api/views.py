from flask import Blueprint, jsonify, request, render_template
import requests
from . import db, logger
from .models import Movie, Search
from . import omdb

main = Blueprint('main', __name__)

## Lena(Yu-Lun) Feature
def fetch_from_movies(query):
    # Clear existing data in Search table
    db.session.query(Search).delete()
    db.session.commit()

    # Encode query for URL
    url_query = requests.utils.quote(query)
    api_url = f"{omdb.base_url}?s={url_query}&apikey={omdb.api_key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        # store_data_in_database(data)
        if 'Search' in data:
            movies = []
            for movie in data['Search']:
                # Ensure you access the keys correctly based on the JSON response structure
                #  These dictionaries are appended to the movies list. The use of movie.get('imdbID', '') and similar lines ensures that if a particular key is not found in the movie data, a default empty string ('') is used instead
                movies.append({
                    'imdbID': movie.get('imdbID', ''),
                    'title': movie.get('Title', ''),
                    'year': movie.get('Year', ''),
                })

                # Create and add each new search result to the database
                new_search_result = Search(
                    imdb_id=movie.get('imdbID'),
                    title=movie.get('Title'),
                    year=movie.get('Year')
                )

                db.session.add(new_search_result)
            
            db.session.commit()  

            return jsonify(movies), 200
        else:
            print("No search results found.")
            return jsonify({'error': 'No search results found'}), 404
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

@main.route('/search_movies', methods=['GET'])
def search_movies():
    # Get the search query from the request
    query = request.args.get('query', '')
    return fetch_from_movies(query)

# 瀏覽我的最愛 Movie Table
@main.route('/movies/favorites', methods=['GET'])
def get_favorites():
    favorites = Movie.query.all()
    favorite_movies = []  # 初始化空列表

    for fav in favorites:
        favorite_movies.append({'imdb_id': fav.imdb_id, 'title': fav.title, 'year': fav.year})

    return jsonify(favorite_movies), 200

def add_movie_to_favorites(imdb_id):
    logger.info(f"Attempting to add movie with imdb_id: {imdb_id} to favorites")

    existing_favorite = Movie.query.filter_by(imdb_id=imdb_id).first()
    if existing_favorite:
        logger.warning(f"Movie with imdb_id: {imdb_id} is already in favorites")
        return {'error': 'Movie already in favorites'}, 409

    movie = Search.query.filter_by(imdb_id=imdb_id).first()
    if not movie:
        logger.error(f"Movie with imdb_id: {imdb_id} not found in search results")
        return {'error': 'Movie not found in search results'}, 404

    new_favorite = Movie(imdb_id=movie.imdb_id, title=movie.title, year=movie.year)
    db.session.add(new_favorite)
    db.session.commit()

    logger.info(f"Movie with imdb_id: {imdb_id} successfully added to favorites")
    return {'message': 'Movie added to favorites'}, 201

@main.route('/add_to_favorites', methods=['POST'])
def add_to_favorites_endpoint():
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON data'}), 400

    data = request.get_json()
    imdb_id = data.get('imdb_id')

    result, status_code = add_movie_to_favorites(imdb_id)
    return jsonify(result), status_code

## Yen's Feature

# Get the Create-new-favorite-movie page
@main.route('/movies/favorite/new', methods=['GET'])
def get_create_page():
    return render_template('create_movie.html') 

# In the Create-new-favorite-movie page, create a new favorite movie
@main.route('/movies/favorite/new', methods=['POST'])
def add_movie():
    if request.is_json:
        # 如果請求是 JSON 格式
        movie_data = request.get_json()

        # 創建新的 Movie 物件
        new_movie = Movie(
            imdb_id=movie_data.get('imdb_id'),
            title=movie_data.get('title'),
            year=movie_data.get('year'),
        )

        # 將新的電影物件添加到數據庫
        db.session.add(new_movie)
        db.session.commit()

        return 'Done', 201
    else:
        return jsonify({'error': 'Invalid JSON data'}), 400

# Get the detail of the specific movie
@main.route('/movies/favorite/<imdb_id>', methods=['GET'])
def movie(imdb_id):
    # 從數據庫中查找電影
    movie = Movie.query.get(imdb_id)

    # 如果電影存在，返回電影數據
    if movie:
        return jsonify({
            'title': movie.title,
            'year': movie.year,
            'imdb_id': movie.imdb_id,
        })
    else:
        # 如果電影不存在，返回 404 錯誤
        return jsonify({'error':'Not found the movie.'}), 404
    
# Get the edit page of the specific movie
@main.route('/movies/favorite/<imdb_id>/edit', methods=['GET'])
def get_edit_page(imdb_id):
    # 從數據庫中查找電影
    movie = Movie.query.get(imdb_id)

    # 如果電影存在，返回 JSON 數據給前端
    if movie:
        return render_template('edit_movie.html', title=movie.title, year=movie.year, imdb_id=movie.imdb_id)
    else:
        return jsonify({'error':'Not found the movie.'}), 404

# In the specific movie edit page, update the movie
@main.route('/movies/favorite/<imdb_id>', methods=['PUT'])
def update_movie(imdb_id):
    # 從數據庫中查找電影
    movie = Movie.query.get(imdb_id)

    # 如果電影存在，更新電影
    if movie:
        movie_data = request.get_json()
        movie.imdb_id = movie_data.get('imdb_id')
        movie.title = movie_data.get('title')
        movie.year = movie_data.get('year')
        db.session.commit()
        return 'Done', 201
    else:
        # 如果電影不存在，返回 404 錯誤
        return jsonify({'error':'Not found the movie.'}), 404

# delete the specific movie
@main.route('/movies/favorite/<imdb_id>', methods=['DELETE'])
def delete_movie(imdb_id):
    # 從數據庫中查找電影
    movie = Movie.query.get(imdb_id)

    # 如果電影存在，刪除電影
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return 'Done', 201
    else:
        # 如果電影不存在，返回 404 錯誤
        return jsonify({'error':'Not found the movie.'}), 404