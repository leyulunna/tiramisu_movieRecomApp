from flask import Blueprint, jsonify, request
import requests
from . import db
from .models import Movie 
from . import omdb

main = Blueprint('main', __name__)

def fetch_and_store_movies():
    api_url = f"{omdb.base_url}?s=Marvel&apikey={omdb.api_key}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        store_data_in_database(data)
        return data
    else:
        return None
    
# 稍待
# @main.route('/favorite_movie', methods=['POST'])
# def favorite_movie():
#     if request.is_json:
#         # 找到使用者選擇的電影＿id
#         movie_id = request.get_json().get('id')
#         # 從資料庫中找到該電影
#         movie = Movie.query.get(movie_id)
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
    

@main.route('/create_a_new_movie', methods=['POST'])
def add_movie():
    if request.is_json:
        # 如果請求是 JSON 格式
        movie_data = request.get_json()

        # 創建新的 Movie 物件
        new_movie = Movie(
            title=movie_data.get('title'),
            year=movie_data.get('year'),
            imdb_id=movie_data.get('imdb_id'),
            poster=movie_data.get('poster')
        )

        # 將新的電影物件添加到數據庫
        db.session.add(new_movie)
        db.session.commit()

        return 'Done', 201
    else:
        return 'Invalid JSON data', 400

@main.route('/movies')
def movies():
    # 從資料庫中獲取所有電影資料
    all_movies = Movie.query.all()

    # 將電影資料轉換為字典格式
    if all_movies:
        formatted_movies = [{
            "id": movie.id,
            "title": movie.title,
            "year": movie.year,
            "imdb_id": movie.imdb_id,
            "poster": movie.poster
        } for movie in all_movies]

        return jsonify({"movies": formatted_movies})
    else:
        return 'No data available', 404

def store_data_in_database(data):
    for movie_data in data['Search']:
        movie = Movie(
            title=movie_data['Title'],
            year=movie_data['Year'],
            imdb_id=movie_data['imdbID'],
            poster=movie_data['Poster']
        )
        db.session.add(movie)

    db.session.commit()

def store_user_data_in_database(user_data):
    # 將用戶提供的數據存儲到數據庫
    movie = Movie(
        title=user_data['Title'],
        year=user_data['Year'],
        imdb_id=user_data['imdbID'],
        poster=user_data['Poster']
    )
    db.session.add(movie)

    db.session.commit()

@main.route('/movies/<movie_id>')
def movie(movie_id):
    # 從數據庫中查找電影
    movie = Movie.query.get(movie_id)

    # 如果電影存在，返回電影數據
    if movie:
        return jsonify({
            'title': movie.title,
            'year': movie.year,
            'imdb_id': movie.imdb_id,
            'poster': movie.poster
        })
    else:
        # 如果電影不存在，返回 404 錯誤
        return 'Not found', 404
    
@main.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    # 從數據庫中查找電影
    movie = Movie.query.get(movie_id)

    # 如果電影存在，刪除電影
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return 'Done', 201
    else:
        # 如果電影不存在，返回 404 錯誤
        return 'Not found', 404
    
@main.route('/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    # 從數據庫中查找電影
    movie = Movie.query.get(movie_id)

    # 如果電影存在，更新電影
    if movie:
        movie_data = request.get_json()
        movie.title = movie_data.get('title')
        movie.year = movie_data.get('year')
        movie.imdb_id = movie_data.get('imdb_id')
        movie.poster = movie_data.get('poster')
        db.session.commit()
        return 'Done', 201
    else:
        # 如果電影不存在，返回 404 錯誤
        return 'Not found', 404
