import pandas as pd
import requests

# 1. 엑셀 데이터(0 포함) 읽기
df = pd.read_excel('통합주소록100.xlsx', dtype=str)

NOTION_TOKEN = "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"
DATABASE_ID = "21cc8a51527e81f7ac69fb658b139d2d"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 2. 노션 DB에서 모든 row(페이지) 가져오기
def get_all_pages(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    results = []
    has_more = True
    next_cursor = None
    while has_more:
        payload = {"page_size": 100}
        if next_cursor:
            payload["start_cursor"] = next_cursor
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        results.extend(data["results"])
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")
    return results

pages = get_all_pages(DATABASE_ID)

# 3. 인덱스 기준으로 매칭하여 전화번호/팩스번호만 업데이트
for page in pages:
    props = page["properties"]
    page_id = page["id"]
    index = str(props["인덱스"]["number"])
    # 엑셀에서 해당 인덱스 row 찾기
    row = df[df["인덱스"] == index].iloc[0]
    phone = row["전화번호"]
    fax = row["팩스번호"]
    patch_url = f"https://api.notion.com/v1/pages/{page_id}"
    patch_data = {
        "properties": {
            "전화번호": {"phone_number": phone},
            "팩스번호": {"phone_number": fax}
        }
    }
    res = requests.patch(patch_url, headers=headers, json=patch_data)
    print(index, phone, fax, res.status_code, res.text) 