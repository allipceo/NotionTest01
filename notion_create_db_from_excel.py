import pandas as pd
import requests

# 1. 엑셀 데이터 읽기
df = pd.read_excel('통합주소록100.xlsx')

# 2. 노션 API 정보
NOTION_TOKEN = "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"  # 첫번째 인테그레이션(노션 MCP연동) Secret
PARENT_PAGE_ID = "21cc8a51527e805e881aef1b86f92a72"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 3. 엑셀 컬럼명 기반으로 노션 속성 정의
def get_notion_property(col):
    if col == "회사명":
        return {"title": {}}
    elif col == "인덱스":
        return {"number": {}}
    else:
        return {"rich_text": {}}

properties = {col: get_notion_property(col) for col in df.columns}

data = {
    "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
    "title": [{"type": "text", "text": {"content": "회사정보 V1.1 (자동생성)"}}],
    "properties": properties
}

response = requests.post("https://api.notion.com/v1/databases", headers=headers, json=data)
print(response.status_code, response.text) 