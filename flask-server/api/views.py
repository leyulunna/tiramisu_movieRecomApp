# from flask import Blueprint, jsonify, request
# from . import db
# from .models import Movie

# main = Blueprint('main', __name__)

# @main.route('/add_movie', methods=['POST'])

# def add_movie():
#   movie_data = request.get_json()

#   new_movie = Movie(title=movie_data['title'], rating=movie_data['rating'])

#   db.session.add(new_movie)
#   db.session.commit()

#   return 'Done', 201

# @main.route('/movies')
# def movies():

#   movies = []

#   return jsonify({'movies' : movies})



# V2
from flask import Blueprint, jsonify, request
from . import jikan_api 
import requests
# from jikan_api import baseUrl  

main = Blueprint('main', __name__)

@main.route('/add_movie', methods=['POST'])
def add_movie():
    # 使用 baseUrl 来构建 API 请求
    api_url = f"{jikan_api.baseUrl}/52034/characters"  # 替换 "your_endpoint_here" 为你要访问的具体 API 端点
    response = requests.get(api_url)
    
    # 处理响应，然后返回结果
    if response.status_code == 200:
        data = response.json()
        # 在这里处理从 API 获取的数据
        return jsonify(data)
    else:
        return 'Failed to fetch data', 500

@main.route('/movies')
def movies():
    movies = []
    return jsonify({'movies' : movies})
