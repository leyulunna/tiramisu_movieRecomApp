from flask import Blueprint, jsonify, request, render_template
import requests
from . import db
from .models import Movie, Favorite
from . import omdb

main = Blueprint('main', __name__)

## Lena(Yu-Lun) Feature
def fetch_from_movies(query):
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
                print(f"Id: {movie['imdbID']}, Title: {movie['Title']}, Year: {movie['Year']}")
                #  These dictionaries are appended to the movies list. The use of movie.get('imdbID', '') and similar lines ensures that if a particular key is not found in the movie data, a default empty string ('') is used instead
                movies.append({
                    'imdbID': movie.get('imdbID', ''),
                    'title': movie.get('Title', ''),
                    'year': movie.get('Year', ''),
                })
            
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

# fetch_from_movies("spider man")

# 加入我的做愛 Table
def add_movie_to_favorites(imdb_id):
    # Check if the movie is already in the favorites
    if Favorite.query.filter_by(imdb_id=imdb_id).first():
        return {'error': 'Movie already in favorites'}, 409

    # Check if movie exists in the Movie table
    movie = Movie.query.filter_by(imdb_id=imdb_id).first()
    if not movie:
        return {'error': 'Movie not found'}, 404

    # Add the movie to favorites
    new_favorite = Favorite(imdb_id=movie.imdb_id, title=movie.title, year=movie.year)
    db.session.add(new_favorite)
    db.session.commit()

    return {'message': 'Movie added to favorites'}, 201

@main.route('/add_to_favorites', methods=['POST'])
def add_to_favorites_endpoint():
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON data'}), 400

    data = request.get_json()
    imdb_id = data.get('imdb_id')

    result, status_code = add_movie_to_favorites(imdb_id)
    return jsonify(result), status_code

# 瀏覽我的最愛 movie
@main.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    for fav in favorites:
        favorite_movies = [
            {'imdb_id': fav.imdb_id, 'title': fav.title, 'year': fav.year}
        ]
    return jsonify(favorite_movies), 200

# 從我的最愛刪除 movie
@main.route('/remove_from_favorites/<imdb_id>', methods=['DELETE'])
def remove_from_favorites(imdb_id):
    favorite = Favorite.query.filter_by(imdb_id=imdb_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Movie removed from favorites'}), 200
    else:
        return jsonify({'error': 'Movie not found in favorites'}), 404

# 稍待
# @main.route('/favorite_movie', methods=['POST'])
# def favorite_movie():
#     if request.is_json:
#         # 找到使用者選擇的電影＿id
#         imdb_id = request.get_json().get('id')
#         # 從資料庫中找到該電影
#         movie = Movie.query.get(imdb_id)
#         # 如果電影存在，將電影資料轉換為字典格式
#         if movie:
#             formatted_movie = {
#                 "id": movie.id,
#                 "title": movie.title,
#                 "year": movie.year,
#                 "imdb_id": movie.imdb_id,
#                 "poster": movie.poster
#             }
#             # 返回電影資料
#             return jsonify(formatted_movie)
#         else:
#             # 如果電影不存在，返回 404 錯誤
#             return 'Not found', 404
#     else:
#         return 'Invalid JSON data', 400

# 以下沒有最後使用到
# def store_data_in_database(data):
#     for movie_data in data['Search']:
#         movie = Movie(
#             title=movie_data['Title'],
#             year=movie_data['Year'],
#             imdb_id=movie_data['imdbID'],
#             poster=movie_data['Poster']
#         )
#         db.session.add(movie)

#     db.session.commit()

# def store_user_data_in_database(user_data):
#     # 將用戶提供的數據存儲到數據庫
#     movie = Movie(
#         title=user_data['Title'],
#         year=user_data['Year'],
#         imdb_id=user_data['imdbID'],
#         # poster=user_data['Poster']
#     )
#     db.session.add(movie)

#     db.session.commit()
    
# Get the favorite page
@main.route('/movies/favorites', methods=['GET'])
def movies():
    # 從資料庫中獲取所有電影資料
    all_movies = Movie.query.all()

    # 將電影資料轉換為字典格式
    if all_movies:
        formatted_movies = [{
            # "id": movie.id,
            "title": movie.title,
            "year": movie.year,
            "imdb_id": movie.imdb_id,
            # "poster": movie.poster
        } for movie in all_movies]

        return jsonify({"movies": formatted_movies})
    else:
        return jsonify({'error': 'No data available'}), 400

# Get the Create-new-favorite-movie page
@main.route('/movies/favorite/new', methods=['GET'])
def get_create_page():
    return render_template('create_movie.html') 

# In the Create-new-favorite-movie page, create the new favorite movie
@main.route('movies/favorite/new', methods=['POST'])
def add_movie():
    if request.is_json:
        # 如果請求是 JSON 格式
        movie_data = request.get_json()

        # 創建新的 Movie 物件
        new_movie = Movie(
            title=movie_data.get('title'),
            year=movie_data.get('year'),
            imdb_id=movie_data.get('imdb_id'),
            # poster=movie_data.get('poster')
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
            # 'poster': movie.poster
        })
    else:
        # 如果電影不存在，返回 404 錯誤
        return jsonify({'error':'Not found the movie.'}), 404
    
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
    
# Get the edit page of the specific movie
@main.route('/movies/favorite/<imdb_id>/edit', methods=['GET'])
def get_edit_page(imdb_id):
    # 從數據庫中查找電影
    movie = Movie.query.get(imdb_id)

    # 如果電影存在，返回 JSON 數據給前端
    if movie:
        return jsonify({
            'title': movie.title,
            'year': movie.year,
            'imdb_id': movie.imdb_id,
            # 'poster': movie.poster
        })
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
        movie.title = movie_data.get('title')
        movie.year = movie_data.get('year')
        movie.imdb_id = movie_data.get('imdb_id')
        # movie.poster = movie_data.get('poster')
        db.session.commit()
        return 'Done', 201
    else:
        # 如果電影不存在，返回 404 錯誤
        return jsonify({'error':'Not found the movie.'}), 404
