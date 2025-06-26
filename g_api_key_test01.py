import requests
r = requests.get(
    "https://www.googleapis.com/customsearch/v1",
    params={
        "key": "AIzaSyDEDD28QmBTFzig_kStW0kJ-FUvzpC3kpc",
        "cx": "475894bdf8f31439d",
        "q": "test"  # 원하는 검색어로 변경 가능
    }
)
print(r.status_code)
print(r.json())