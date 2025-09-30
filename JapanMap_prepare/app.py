from geopy.exc import GeocoderUnavailable
import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import os

#データ読み込み
def load_data():
    base_path = os.path.dirname(__file__)  # ここで app.py の場所
    file_path = os.path.join(base_path, "非チェーン店リスト.csv")
    df = pd.read_csv(file_path)
    return pd.read_csv(file_path)

# ✅ ここで必ず読み込む
df = load_data()

# サイト名（タイトル部分）
st.markdown(
    """
    <h1 style='text-align: center; color: #FFD700;'>
        YumYum
    </h1>
    <p style='text-align: center; color: #AAAAAA;'>
        全国の個人経営・非チェーン飲食店を検索できるデータベース
    </p>
    <hr style="border: 1px solid #444;">
    """,
    unsafe_allow_html=True
)

#検索条件を中央に配置
col1, col2, col3 = st.columns([1, 2, 1])  # 真ん中を広めに
#with col2:
st.subheader("Search")
# 都道府県の選択肢
# 都道府県入力（「すべて」も自由記入で対応）
pref = st.text_input("都道府県を入力（例：東京都、大阪府、沖縄県、すべて）", "すべて").strip()


#プルダウンで選択 or 自由入力
#pref_selected = st.selectbox("都道府県を選択（または下の入力欄に直接入力）", pref_options)
#pref_input = st.text_input("自由入力（例：東京都、大阪府、沖縄県）")

# 「すべて」かプルダウンで選んだ都道府県、または自由入力を優先
#if pref_input.strip():
    #pref = pref_input.strip()
#else:
    #pref = pref_selected
genre = st.text_input("ジャンル（例：ラーメン、寿司、カフェ）")
keyword = st.text_input("キーワード（店名など）")
st.markdown("<br>", unsafe_allow_html=True)  # 余白
search_button = st.button("検索する 🚀")

# データフィルタ
filtered_df = df.copy()

if pref != "すべて":
    filtered_df = filtered_df[filtered_df["都道府県"] == pref]

if genre:
    filtered_df = filtered_df[filtered_df["ジャンル"].astype(str).str.contains(genre, na=False)]

if keyword:
    # 複数列を文字列に変換して結合（NaNは空文字に）
    search_cols = ["name", "ジャンル", "都道府県", "住所", "Googleマップ"]
    filtered_df = filtered_df[
    filtered_df[search_cols]
    .astype(str)
    .apply(lambda row: " ".join(row), axis=1)  # 行方向に結合
    .str.contains(keyword, na=False, case=False)  # 部分一致検索
    ]


st.write(f"### 検索結果: {len(filtered_df)} 件")
st.dataframe(filtered_df[["name", "ジャンル", "都道府県", "住所", "Googleマップ"]])

# ==============================
# 地図表示（検索結果の最初の1件だけを例として表示）
#if len(filtered_df) > 0:
    #address = filtered_df.iloc[0]["住所"]
    #st.write(f"地図表示: {filtered_df.iloc[0]['name']} ({address})")

    #geolocator = Nominatim(user_agent="non_chain_locator")
    #location = geolocator.geocode(str(address) + ", Japan")

    #if location:
        #lat, lng = location.latitude, location.longitude
        #m = folium.Map(location=[lat, lng], zoom_start=14)
        #folium.Marker([lat, lng], popup=filtered_df.iloc[0]["name"]).add_to(m)
        #st_folium(m, width=700, height=500)
    #else:
        #st.warning("この住所から座標を取得できませんでした。")

import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# 地図表示（検索結果の最初の1件だけ例示）
#if len(filtered_df) > 0:
    #address = filtered_df.iloc[0]["住所"]
    #st.write(f"地図表示: {filtered_df.iloc[0]['name']} ({address})")

    #geolocator = Nominatim(user_agent="non_chain_locator")
    #location = None
    #if address and str(address) != "nan":
        #location = geolocator.geocode(str(address) + ", Japan")

    #if location:
        #lat, lng = location.latitude, location.longitude
    #else:
        # ★ フォールバック（東京駅）
        #st.warning("この住所から座標を取得できませんでした。代わりに東京駅を表示します。")
        #lat, lng = 35.681236, 139.767125  # 東京駅

    # 地図を作成
    #m = folium.Map(location=[lat, lng], zoom_start=14)
    #folium.Marker([lat, lng], popup=filtered_df.iloc[0]["name"]).add_to(m)

    # streamlit-folium で埋め込み
    #st_data = st_folium(m, width=700, height=500)

    # 地図クリックで座標取得
    #if st_data and st_data["last_clicked"]:
        #st.write("クリック位置:", st_data["last_clicked"])


import re
import tqdm
import folium
import requests
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

if len(filtered_df) > 0:
    # 検索結果から選択できる UI を追加
    options = filtered_df["name"].tolist()
    selected_name = st.selectbox("地図を表示する店舗を選んでください", options)

    # 選択された行を取得
    selected_row = filtered_df[filtered_df["name"] == selected_name].iloc[0]
    address = selected_row["住所"]

    st.write(f"地図表示: {selected_row['name']} ({address})")

   # ジオコーディング
geolocator = Nominatim(user_agent="non_chain_locator")
location = None

try:
    if address and str(address) != "nan":
        simple_address = address.split("丁目")[0]  # 「丁目」以降を削除
        location = geolocator.geocode(simple_address + ", Japan")

    if location:
        lat, lng = location.latitude, location.longitude
    else:
        st.warning("この住所から座標を取得できませんでした。代わりに東京駅を表示します。")
        lat, lng = 35.681236, 139.767125  # 東京駅

except GeocoderUnavailable:
    st.error("ジオコーディングサービスに接続できませんでした。後でもう一度試してください。")
    # フォールバックとして東京駅
    lat, lng = 35.681236, 139.767125

    # 地図を作成
    m = folium.Map(location=[lat, lng], zoom_start=14)
    folium.Marker([lat, lng], popup=selected_row["name"]).add_to(m)

    # Streamlit で表示
    st_folium(m, width=700, height=500)

#DataFrame 表示（検索結果)
#st.write(f"検索結果: {len(filtered_df)} 件")
#import requests
#url = f"https://maps.googleapis.com/maps/api/geocode/json"
#params = {"address": address, "key": API_KEY}
#res = requests.get(url, params=params).json()
#if res["status"] == "OK":
    #loc = res["results"][0]["geometry"]["location"]
    #lat, lng = loc["lat"], loc["lng"]


# 表をクリック可能に
#edited = st.data_editor(
    #filtered_df[["name", "ジャンル", "都道府県", "住所"]],
    #hide_index=True,
    #use_container_width=True,
    #disabled=True  # ←編集はさせずクリックだけ
#)

with st.form("add_store"):
    name = st.text_input("店名")
    address = st.text_input("住所")
    genre = st.text_input("ジャンル")
    submitted = st.form_submit_button("Post")

    if submitted:
        new_row = {"name": name, "住所": address, "ジャンル": genre}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("非チェーン店リスト.csv", index=False, encoding="utf-8-sig")
        st.success("店舗を追加しました！")
        st.rerun()
#st.write(f"検索結果: {len(df)} 件")

