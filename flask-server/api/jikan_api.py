# terminal: 
# pip install pipenv
# pipenv install
# pipenv shell
# pipenv install flask flask-sqlalchemy
# export FLASK_APP=api
# export FLASK_DEBUG=1

import requests

# baseUrl = 'https://api.jikan.moe/v4/anime?q=Naruto&sfw'

baseUrl = 'https://api.jikan.moe/v4/anime'

endpoint = '52034/characters'

movies_data = requests.get(baseUrl)

movies_data = movies_data.json()

# print(movies_data)