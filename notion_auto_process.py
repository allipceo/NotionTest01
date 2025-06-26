import os
import time
import json
from notion_client import Client
from rapidfuzz import fuzz
from tqdm import tqdm

# 환경설정
NOTION_TOKEN = "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"
NOTION_DB_ID = "21cc8a51-527e-81f7-ac69-fb658b139d2d"
BACKUP_PATH = "./notion_backup_1.json"

notion = Client(auth=NOTION_TOKEN)

# 1. 노션 DB 전체 백업
def backup_notion_db():
    results = []
    next_cursor = None
    while True:
        response = notion.databases.query(
            database_id=NOTION_DB_ID,
            start_cursor=next_cursor
        )
        results.extend(response['results'])
        next_cursor = response.get('next_cursor')
        if not next_cursor:
            break
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[백업] 노션 DB 전체 백업 완료 ({len(results)}건)")

# 2. 기존 데이터 로딩
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

# 3. 중복 제거 로직 (사업자등록번호, 회사명 유사도 등)
def remove_duplicates(data):
    seen = {}
    unique = []
    for row in data:
        reg_num = row['properties']['사업자등록번호']['rich_text'][0]['plain_text']
        company = row['properties']['회사명']['title'][0]['plain_text']
        if reg_num in seen:
            prev_company = seen[reg_num]['properties']['회사명']['title'][0]['plain_text']
            sim = fuzz.WRatio(company, prev_company)
            if sim >= 90:
                continue
        seen[reg_num] = row
        unique.append(row)
    return unique

# 4. 회사ID 필드 생성 및 부여
def assign_company_ids(data):
    for idx, row in enumerate(data, 1):
        company_id = f"CO-{idx:05d}"
        notion.pages.update(
            page_id=row['id'],
            properties={
                "회사ID": {
                    "rich_text": [{"text": {"content": company_id}}]
                }
            }
        )
        if idx % 10 == 0:
            print(f"[진행] {idx}건 처리 완료")
        time.sleep(1)  # Rate Limit 대응
    print(f"[회사ID] {len(data)}건 순차 ID 부여 완료")

# 5. 전체 실행
def main():
    print("[1차 작업] 노션 DB 백업 시작")
    backup_notion_db()
    print("[1차 작업] 기존 데이터 로딩")
    data = load_notion_data()
    print(f"[1차 작업] 총 {len(data)}건 로딩")
    print("[1차 작업] 중복 제거")
    unique = remove_duplicates(data)
    print(f"[1차 작업] 중복 제거 후 {len(unique)}건")
    print("[1차 작업] 회사ID 부여")
    assign_company_ids(unique)
    print("[1차 작업] 완료")

if __name__ == "__main__":
    main() 