import requests
from notion_client import Client
from datetime import datetime

# 구글 Custom Search API 정보
GOOGLE_API_KEY = "AIzaSyDEDD28QmBTFzig_kStW0kJ-FUvzpC3kpc"
GOOGLE_CX = "475894bdf8f31439d"

# 노션 API 정보
NOTION_TOKEN = "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"
NOTION_DB_ID = "21cc8a51527e80dcb1f9ed1d7eebd2ec"

# 1. 구글 뉴스 API로 뉴스 데이터 수집 (에너지 키워드 예시)
def fetch_google_news(query, num=1):
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
        print("구글 뉴스 API 오류:", res.text)
        return []

# 2. 노션 DB에 뉴스 데이터 업로드
def upload_to_notion(news_item):
    notion = Client(auth=NOTION_TOKEN)
    today = datetime.today().strftime("%Y-%m-%d")
    notion.pages.create(
        parent={"database_id": NOTION_DB_ID},
        properties={
            "제목": {"title": [{"text": {"content": news_item.get("title", "구글뉴스")}}]},
            "발행일": {"date": {"start": today}},
            "URL": {"url": news_item.get("link", "")},
            "분야": {"select": {"name": "에너지"}},
            "세부키워드": {"multi_select": [{"name": "구글뉴스"}]},
            "중요도": {"select": {"name": "중간"}},
            "요약": {"rich_text": [{"text": {"content": news_item.get("snippet", "")}}]},
            "읽음": {"checkbox": False}
        }
    )

if __name__ == "__main__":
    news_list = fetch_google_news("에너지", num=1)
    for news in news_list:
        upload_to_notion(news)
    print("구글 뉴스 1건을 노션 DB에 업로드 완료!") 