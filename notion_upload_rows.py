import pandas as pd
import requests

# 1. 엑셀 데이터 읽기
df = pd.read_excel('통합주소록100.xlsx')

# 2. 노션 API 정보
NOTION_TOKEN = "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"  # 사용한 인테그레이션 Secret
DATABASE_ID = "21cc8a51527e81f7ac69fb658b139d2d"  # 새로 생성된 데이터베이스의 ID

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 3. 데이터 업로드
for _, row in df.iterrows():
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "인덱스": {"number": int(row["인덱스"])},
            "회사명": {"title": [{"text": {"content": str(row["회사명"])}}]},
            "사업자등록번호": {"rich_text": [{"text": {"content": str(row["사업자등록번호"])}}]},
            "팩스번호": {"rich_text": [{"text": {"content": str(row["팩스번호"])}}]},
            "전화번호": {"rich_text": [{"text": {"content": str(row["전화번호"])}}]},
            "대표이사": {"rich_text": [{"text": {"content": str(row["대표이사"])}}]},
        }
    }
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
    print(response.status_code, response.text) 