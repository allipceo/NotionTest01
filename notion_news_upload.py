import requests
from notion_client import Client
from datetime import datetime
import time

# 네이버 뉴스 API 정보
NAVER_CLIENT_ID = "7PEImiCz3n9XSv35tNXK"
NAVER_CLIENT_SECRET = "GjPic6dQrl"

# 구글 Custom Search API 정보
GOOGLE_API_KEY = "AIzaSyDEDD28QmBTFzig_kStW0kJ-FUvzpC3kpc"
GOOGLE_CX = "475894bdf8f31439d"

# 노션 API 정보
NOTION_TOKEN = "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"
NOTION_DB_ID = "21cc8a51527e80dcb1f9ed1d7eebd2ec"

KEYWORDS = [
    ("방위산업", "방산"),
    ("신재생에너지", "에너지"),
    ("보험중개", "보험")
]

# 네이버 뉴스 API로 뉴스 데이터 수집
def fetch_naver_news(query, display=3):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {"query": query, "display": display}
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        return res.json().get("items", [])
    else:
        print(f"네이버 뉴스 API 오류({query}):", res.text)
        return []

# 구글 뉴스 API로 뉴스 데이터 수집
def fetch_google_news(query, num=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "num": num,
        "sort": "date"
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json().get("items", [])
    else:
        print(f"구글 뉴스 API 오류({query}):", res.text)
        return []

# 노션 DB에 뉴스 데이터 업로드
def upload_to_notion(news_item, 분야, source="네이버"):
    notion = Client(auth=NOTION_TOKEN)
    today = datetime.today().strftime("%Y-%m-%d")
    # 네이버/구글 데이터 구조 차이 보정
    if source == "네이버":
        title = news_item.get("title", "")
        url = news_item.get("link", "")
        summary = news_item.get("description", "")
        keyword_tag = "네이버뉴스"
    else:
        title = news_item.get("title", "")
        url = news_item.get("link", "")
        summary = news_item.get("snippet", "")
        keyword_tag = "구글뉴스"
    notion.pages.create(
        parent={"database_id": NOTION_DB_ID},
        properties={
            "제목": {"title": [{"text": {"content": title}}]},
            "발행일": {"date": {"start": today}},
            "URL": {"url": url},
            "분야": {"select": {"name": 분야}},
            "세부키워드": {"multi_select": [{"name": keyword_tag}]},
            "중요도": {"select": {"name": "중간"}},
            "요약": {"rich_text": [{"text": {"content": summary}}]},
            "읽음": {"checkbox": False}
        }
    )
    print(f"{source} 뉴스 업로드 완료: {title}")
    time.sleep(0.5)  # API rate limit 방지

if __name__ == "__main__":
    for keyword, 분야 in KEYWORDS:
        # 네이버 뉴스 3개
        naver_news = fetch_naver_news(keyword, display=3)
        for news in naver_news:
            upload_to_notion(news, 분야, source="네이버")
        # 구글 뉴스 3개
        google_news = fetch_google_news(keyword, num=3)
        for news in google_news:
            upload_to_notion(news, 분야, source="구글")
    print("총 18개(네이버/구글 각 9개) 뉴스 업로드 완료!") 