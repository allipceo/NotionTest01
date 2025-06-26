import time
from notion_client import Client

NOTION_TOKEN = "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"
NOTION_DB_ID = "21cc8a51-527e-81f7-ac69-fb658b139d2d"

notion = Client(auth=NOTION_TOKEN)

# 노션 DB 데이터 로딩
def load_notion_data():
    data = []
    next_cursor = None
    while True:
        response = notion.databases.query(
            database_id=NOTION_DB_ID,
            start_cursor=next_cursor
        )
        data.extend(response['results'])
        next_cursor = response.get('next_cursor')
        if not next_cursor:
            break
    return data

# 회사ID 순서대로 정렬 후 인덱스 부여
def update_index():
    data = load_notion_data()
    # 회사ID 기준 정렬
    def id_key(row):
        cid = row['properties']['회사ID']['rich_text'][0]['plain_text']
        return int(cid.split('-')[1])
    sorted_rows = sorted([r for r in data if r['properties']['회사ID']['rich_text']], key=id_key)
    for idx, row in enumerate(sorted_rows, 1):
        notion.pages.update(
            page_id=row['id'],
            properties={
                "인덱스": {
                    "number": idx
                }
            }
        )
        if idx % 10 == 0:
            print(f"[인덱스] {idx}번까지 자동 입력 완료")
        time.sleep(1)
    print(f"[인덱스] 총 {len(sorted_rows)}건 자동 입력 완료")

if __name__ == "__main__":
    update_index() 