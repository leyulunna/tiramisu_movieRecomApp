import requests

api_key = '4f77437e'
base_url = 'https://www.omdbapi.com/'

# 使用搜尋功能，尋找 Marvel 相關的電影
search_params = {'s': 'Marvel', 'apikey': api_key}
movies_data = requests.get(base_url, params=search_params)

# 將回傳的內容轉換為 JSON 格式
movies_data = movies_data.json()

# 打印結果
print(movies_data)
