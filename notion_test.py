import os
from notion_client import Client
from dotenv import load_dotenv

# 환경 변수 로드
def main():
    load_dotenv()
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("NOTION_TOKEN 환경변수가 설정되어 있지 않습니다. .env 파일을 확인하세요.")
        return
    notion = Client(auth=notion_token)

    # 사용자가 제공한 Notion DB 링크에서 DB ID 추출
    # 링크: https://www.notion.so/21bc8a51527e8054a0c0dfc4a03b46d3?v=21bc8a51527e80c5a903000c13bd4334&source=copy_link
    database_id = "21bc8a51527e8054a0c0dfc4a03b46d3"

    try:
        response = notion.databases.query(database_id=database_id)
        print("쿼리 결과:")
        print(response)
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main() 