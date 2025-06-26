import requests
headers = {
    "X-Naver-Client-Id": "7PEImiCz3n9XSv35tNXK",
    "X-Naver-Client-Secret": "GjPic6dQrl"
}
r = requests.get("https://openapi.naver.com/v1/search/blog", params={"query": "테스트"}, headers=headers)
print("유효" if r.status_code == 200 else "무효") 