import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from crawler import search_site_links

load_dotenv()

app = Flask(__name__)

# サンプル地点。追加する場合は id を重複させず、公式サイトURLと座標を確認してください。
LOCATIONS = [
    {
        "id": 1,
        "name": "東京タワー",
        "lat": 35.6586,
        "lng": 139.7454,
        "url": "https://www.tokyotower.co.jp/",
        "schedule": "営業時間・イベント情報は公式サイトで確認してください。",
        "description": "施設の案内は公式サイトをご確認ください。",
        "features": "施設・サービスの詳細は公式サイトをご確認ください。",
    },
    {
        "id": 2,
        "name": "東京駅",
        "lat": 35.6812,
        "lng": 139.7671,
        "url": "https://www.jreast.co.jp/estation/stations/1039.html",
        "schedule": "運行・施設情報は公式サイトで確認してください。",
        "description": "駅や周辺施設の案内は公式サイトをご確認ください。",
        "features": "施設・サービスの詳細は公式サイトをご確認ください。",
    },
    {
        "id": 3,
        "name": "新宿御苑",
        "lat": 35.6852,
        "lng": 139.7100,
        "url": "https://www.env.go.jp/garden/shinjukugyoen/",
        "schedule": "開園時間・イベント情報は公式サイトで確認してください。",
        "description": "施設の案内は公式サイトをご確認ください。",
        "features": "施設・サービスの詳細は公式サイトをご確認ください。",
    },
]

LOCATIONS_BY_ID = {str(item["id"]): item for item in LOCATIONS}


@app.get("/")
def index():
    return render_template(
        "index.html",
        api_key=os.getenv("GOOGLE_MAPS_API_KEY", "").strip(),
        locations=LOCATIONS,
    )


@app.get("/api/search")
def api_search():
    location_id = request.args.get("location_id", "").strip()
    keyword = request.args.get("keyword", "").strip()
    location = LOCATIONS_BY_ID.get(location_id)

    if location is None:
        return jsonify({"error": "登録済みの地点を選択してください。", "results": []}), 400
    if not keyword:
        return jsonify({"error": "検索キーワードを入力してください。", "results": []}), 400
    if len(keyword) > 100:
        return jsonify({"error": "検索キーワードは100文字以内で入力してください。", "results": []}), 400

    results = search_site_links(location["url"], keyword)
    return jsonify({"results": results})


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, host="127.0.0.1", port=int(os.getenv("PORT", "5000")))
