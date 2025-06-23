import os
import requests
from dotenv import load_dotenv

load_dotenv()
claude_api_key = os.getenv("CLAUDE_API_KEY")

# Claude API 호출 예시
url = "https://api.anthropic.com/v1/messages"
headers = {
    "x-api-key": claude_api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}
data = {
    "model": "claude-3-opus-20240229",  # 또는 사용 가능한 모델명
    "max_tokens": 256,
    "messages": [
        {"role": "user", "content": "안녕하세요, 클로드! 간단히 자기소개 해주세요."}
    ]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())