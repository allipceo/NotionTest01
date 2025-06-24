"""
엑셀→노션 자동화 표준 템플릿
- 전화번호 0 누락 방지
- 함수화/재사용 구조
- 5분 매뉴얼 포함
"""
import pandas as pd
import requests

def excel_to_notion(excel_path, notion_token, database_id, column_map):
    """
    엑셀 데이터를 노션 데이터베이스로 업로드하는 표준 함수
    - excel_path: 엑셀 파일 경로
    - notion_token: 노션 인테그레이션 키
    - database_id: 노션 데이터베이스 ID
    - column_map: {'엑셀컬럼명': 'notion_type'} (notion_type: 'title', 'number', 'rich_text', 'phone_number')
    """
    df = pd.read_excel(excel_path, dtype=str)  # 0 누락 방지
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    for _, row in df.iterrows():
        properties = {}
        for excel_col, notion_type in column_map.items():
            if notion_type == "title":
                properties[excel_col] = {"title": [{"text": {"content": row[excel_col]}}]}
            elif notion_type == "number":
                properties[excel_col] = {"number": int(row[excel_col])}
            elif notion_type == "phone_number":
                properties[excel_col] = {"phone_number": row[excel_col]}
            else:
                properties[excel_col] = {"rich_text": [{"text": {"content": row[excel_col]}}]}
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
        print(response.status_code, response.text)

if __name__ == "__main__":
    # 5분 매뉴얼 예시
    # 1. 엑셀 파일명, 노션 키, 데이터베이스 ID, 컬럼 매핑만 입력
    excel_path = "통합주소록100.xlsx"
    notion_token = "여기에_노션_키"
    database_id = "여기에_데이터베이스_ID"
    column_map = {
        "인덱스": "number",
        "회사명": "title",
        "사업자등록번호": "rich_text",
        "팩스번호": "phone_number",
        "전화번호": "phone_number",
        "대표이사": "rich_text"
    }
    excel_to_notion(excel_path, notion_token, database_id, column_map) 