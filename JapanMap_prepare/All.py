import math
import requests
import time

API_KEY = "AIzaSyBGgnq8e3ow0DWvbwPHiaWN61Sy0AXnStg"
radius_km = 2
lat_step_factor = 0.9
pref_coords = {
    "北海道": (43.0642, 141.3469),
    "青森県": (40.8244, 140.74),
    "岩手県": (39.7036, 141.1527),
    "宮城県": (38.2688, 140.8721),
    "秋田県": (39.7186, 140.1024),
    "山形県": (38.2404, 140.3633),
    "福島県": (37.7503, 140.4676),
    "茨城県": (36.3418, 140.4468),
    "栃木県": (36.5657, 139.8836),
    "群馬県": (36.3912, 139.0609),
    "埼玉県": (35.8569, 139.6489),
    "千葉県": (35.6046, 140.1233),
    "東京都": (35.6895, 139.6917),
    "神奈川県": (35.4478, 139.6425),
    "新潟県": (37.9026, 139.0236),
    "富山県": (36.6953, 137.2113),
    "石川県": (36.5947, 136.6256),
    "福井県": (36.0652, 136.2216),
    "山梨県": (35.6639, 138.5684),
    "長野県": (36.6513, 138.181),
    "岐阜県": (35.3912, 136.7223),
    "静岡県": (34.9769, 138.3831),
    "愛知県": (35.1802, 136.9066),
    "三重県": (34.7303, 136.5086),
    "滋賀県": (35.0045, 135.8686),
    "京都府": (35.0214, 135.7556),
    "大阪府": (34.6937, 135.5023),
    "兵庫県": (34.6913, 135.183),
    "奈良県": (34.6851, 135.8048),
    "和歌山県": (34.226, 135.1675),
    "鳥取県": (35.5011, 134.2351),
    "島根県": (35.4723, 133.0505),
    "岡山県": (34.6618, 133.935),
    "広島県": (34.3963, 132.4596),
    "山口県": (34.1859, 131.4714),
    "徳島県": (34.0658, 134.5593),
    "香川県": (34.3401, 134.0434),
    "愛媛県": (33.8416, 132.7657),
    "高知県": (33.5597, 133.5311),
    "福岡県": (33.6064, 130.4181),
    "佐賀県": (33.2494, 130.2988),
    "長崎県": (32.7448, 129.8737),
    "熊本県": (32.7898, 130.7417),
    "大分県": (33.2382, 131.6126),
    "宮崎県": (31.9111, 131.4239),
    "鹿児島県": (31.5602, 130.5581),
    "沖縄県": (26.2124, 127.6809)
}

pref_area_dict = {
    "北海道": 83456,
    "青森県": 9646,
    "岩手県": 15275,
    "宮城県": 7282,
    "秋田県": 11638,
    "山形県": 9323,
    "福島県": 13784,
    "茨城県": 6097,
    "栃木県": 6408,
    "群馬県": 6362,
    "埼玉県": 3798,
    "千葉県": 5157,
    "東京都": 2194,
    "神奈川県": 2416,
    "新潟県": 12584,
    "富山県": 4248,
    "石川県": 4186,
    "福井県": 4190,
    "山梨県": 4465,
    "長野県": 13562,
    "岐阜県": 10621,
    "静岡県": 7777,
    "愛知県": 5172,
    "三重県": 5774,
    "滋賀県": 4017,
    "京都府": 4613,
    "大阪府": 1905,
    "兵庫県": 8400,
    "奈良県": 3691,
    "和歌山県": 4726,
    "鳥取県": 3507,
    "島根県": 6708,
    "岡山県": 7114,
    "広島県": 8479,
    "山口県": 6113,
    "徳島県": 4146,
    "香川県": 1877,
    "愛媛県": 5676,
    "高知県": 7104,
    "福岡県": 4986,
    "佐賀県": 2440,
    "長崎県": 4132,
    "熊本県": 7409,
    "大分県": 6341,
    "宮崎県": 7736,
    "鹿児島県": 9187,
    "沖縄県": 2281
}

# メインタイプ（飲食カテゴリ分類）
types = ["restaurant", "cafe", "bar", "bakery", "meal_takeaway"]

# ジャンル補完（店名に現れるワード）
keywords = [
    "クレープ",
    "中華そば",
    "麺",
    "たこ焼き",
    "唐揚げ",
    "寿司"
]

for pref, (base_lat, base_lng) in pref_coords.items():
    area = pref_area_dict[pref]
    radius = radius_km * 1000  # m

    # ステップ算出
    lat_step = (radius_km / 111) * lat_step_factor
    lng_step = (radius_km / (111 * math.cos(math.radians(base_lat)))) * lat_step_factor

    # 必要なグリッド数
    needed_requests = math.ceil(area / (math.pi * radius_km**2))
    n_points = math.ceil(math.sqrt(needed_requests))

    print(f"▶ {pref} - 推定リクエスト数: {needed_requests}")

    for i in range(n_points):
        for j in range(n_points):
            lat = base_lat + i * lat_step
            lng = base_lng + j * lng_step
            location = f"{lat},{lng}"

            # typeベースの取得
            for t in types:
                params = {
                    "location": location,
                    "radius": radius,
                    "type": t,
                    "key": API_KEY
                }
                response = requests.get(
                    "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=params)
                results = response.json().get("results", [])
                for r in results:
                    print(f"{pref} ({t}) - {r['name']} - {r.get('vicinity', '住所不明')}")

                # 次ページ対応（最大3ページ）
                next_page = response.json().get("next_page_token")
                while next_page:
                    time.sleep(2)
                    params["pagetoken"] = next_page
                    response = requests.get(
                        "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=params)
                    results = response.json().get("results", [])
                    for r in results:
                        print(f"{pref} ({t}) - {r['name']} - {r.get('vicinity', '住所不明')}")
                    next_page = response.json().get("next_page_token")
                time.sleep(1)

            # keywordベースの取得
            for kw in keywords:
                params = {
                    "location": location,
                    "radius": radius,
                    "keyword": kw,
                    "key": API_KEY
                }
                response = requests.get(
                    "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=params)
                results = response.json().get("results", [])
                for r in results:
                    print(f"{pref} (kw:{kw}) - {r['name']} - {r.get('vicinity', '住所不明')}")

                next_page = response.json().get("next_page_token")
                while next_page:
                    time.sleep(2)
                    params["pagetoken"] = next_page
                    response = requests.get(
                        "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=params)
                    results = response.json().get("results", [])
                    for r in results:
                        print(f"{pref} (kw:{kw}) - {r['name']} - {r.get('vicinity', '住所不明')}")
                    next_page = response.json().get("next_page_token")
                time.sleep(1)
