from flask import Flask, render_template, request
import requests, re, statistics
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_year(text):
    text = text.upper()
    match = re.findall(r'([12][0-9]{1}(AW|SS))', text)
    return match[0][0] if match else None

def extract_price(text):
    match = re.search(r'(\d{1,3}(?:,\d{3})*)円', text)
    return int(match.group(1).replace(',', '')) if match else None

# --- 各サイト検索関数（シンプル版） ---
def search_mercari(code):
    # 実際にはHTML構造の変化により結果取得が不安定なので、デモ用ダミーデータ
    return [("22AW", 28000), ("22AW", 30000), ("21AW", 25000)]

def search_yahoo(code):
    return [("22AW", 27000), ("22AW", 29500)]

def search_rakuten(code):
    return [("22AW", 31000), ("21AW", 26000)]

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        code = request.form["code"]

        data = search_mercari(code) + search_yahoo(code) + search_rakuten(code)
        years = [y for y, _ in data]
        prices = [p for _, p in data]

        if years:
            most_common = max(set(years), key=years.count)
            score = int(years.count(most_common) / len(years) * 100)
            avg_price = int(statistics.mean(prices)) if prices else 0
        else:
            most_common, score, avg_price = "年式不明", 0, 0

        result = {
            "code": code,
            "year": most_common,
            "score": score,
            "avg_price": avg_price
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
