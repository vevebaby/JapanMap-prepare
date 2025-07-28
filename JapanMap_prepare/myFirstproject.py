import requests

API_KEY = 'AIzaSyBGgnq8e3ow0DWvbwPHiaWN61Sy0AXnStg'
location = '35.681236,139.767125'  # 東京駅
radius = 1000  # 半径1km
keyword = '居酒屋'

url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    "location": location,
    "radius": radius,
    "keyword": keyword,
    "key": API_KEY
}

response = requests.get(url, params=params)
results = response.json()["results"]

for r in results:
    print(r["name"], "-", r["vicinity"])
