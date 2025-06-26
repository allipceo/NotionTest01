import os
import time
import json
import pandas as pd
from notion_client import Client
from rapidfuzz import fuzz
from tqdm import tqdm

# 환경설정
NOTION_TOKEN = "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"
NOTION_DB_ID = "21cc8a51-527e-81f7-ac69-fb658b139d2d"
EXCEL_PATH = "통합주소록100-2.xlsx"

notion = Client(auth=NOTION_TOKEN)

# 1. 엑셀 데이터 로딩 및 전처리
def load_excel_data():
    df = pd.read_excel(EXCEL_PATH, dtype=str)
    df = df.fillna("")  # 공란 제거
    return df

# 2. 노션 DB 기존 데이터 로딩
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

# 3. 중복 검증 (사업자등록번호, 회사명 유사도 등)
def is_duplicate(row, notion_data):
    reg_num = row['사업자등록번호']
    company = row['회사명']
    for n in notion_data:
        n_reg = n['properties']['사업자등록번호']['rich_text'][0]['plain_text']
        n_company = n['properties']['회사명']['title'][0]['plain_text']
        if reg_num == n_reg:
            return True
        sim = fuzz.WRatio(company, n_company)
        if sim >= 90:
            return True
    return False

# 4. 노션에 신규 데이터 업로드 (회사ID는 비워둠)
def upload_new_rows(df, notion_data):
    uploaded = 0
    for idx, row in df.iterrows():
        if is_duplicate(row, notion_data):
            continue
        props = {
            "회사명": {"title": [{"text": {"content": row['회사명']}}]},
            "사업자등록번호": {"rich_text": [{"text": {"content": row['사업자등록번호']}}]},
            "전화번호": {"phone_number": row['전화번호']},
            "팩스번호": {"phone_number": row['팩스번호']},
            "대표이사": {"rich_text": [{"text": {"content": row['대표이사']}}]},
            # 회사ID는 비워둠
        }
        notion.pages.create(parent={"database_id": NOTION_DB_ID}, properties=props)
        uploaded += 1
        if uploaded % 10 == 0:
            print(f"[진행] {uploaded}건 신규 업로드 완료")
        time.sleep(1)  # Rate Limit
    print(f"[신규 업로드] 총 {uploaded}건 완료")

# 5. 회사ID가 비어 있는 행에 대해 자동 부여
def assign_company_ids():
    data = load_notion_data()
    # 회사ID가 비어 있는 행만 추출
    empty_id_rows = [row for row in data if not row['properties']['회사ID']['rich_text']]
    start_idx = len(data) - len(empty_id_rows) + 1
    for i, row in enumerate(empty_id_rows, start=start_idx):
        company_id = f"CO-{i:05d}"
        notion.pages.update(
            page_id=row['id'],
            properties={
                "회사ID": {
                    "rich_text": [{"text": {"content": company_id}}]
                }
            }
        )
        if (i - start_idx + 1) % 10 == 0:
            print(f"[회사ID] {i}번까지 자동 부여 완료")
        time.sleep(1)
    print(f"[회사ID] 신규 {len(empty_id_rows)}건 자동 부여 완료")

# 6. 전체 실행
def main():
    print("[2,3차 작업] 엑셀 데이터 로딩 및 전처리")
    df = load_excel_data()
    print(f"[2,3차 작업] 엑셀 데이터 {len(df)}건 로딩")
    print("[2,3차 작업] 노션 DB 기존 데이터 로딩")
    notion_data = load_notion_data()
    print(f"[2,3차 작업] 노션 DB {len(notion_data)}건 로딩")
    print("[2,3차 작업] 신규 데이터 업로드 시작")
    upload_new_rows(df, notion_data)
    print("[2,3차 작업] 회사ID 자동 부여 시작")
    assign_company_ids()
    print("[2,3차 작업] 완료")

if __name__ == "__main__":
    main() 