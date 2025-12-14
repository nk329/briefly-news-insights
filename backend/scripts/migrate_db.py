"""
데이터베이스 마이그레이션 스크립트
RDS에 테이블을 자동으로 생성합니다.
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, engine
from sqlalchemy import inspect

def check_tables():
    """현재 데이터베이스에 있는 테이블 목록 확인"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return tables

def main():
    """메인 함수"""
    print("=" * 50)
    print("데이터베이스 마이그레이션 시작")
    print("=" * 50)
    
    # 현재 테이블 확인
    print("\n[1단계] 현재 데이터베이스 테이블 확인...")
    try:
        existing_tables = check_tables()
        print(f"기존 테이블: {existing_tables if existing_tables else '(없음)'}")
    except Exception as e:
        print(f"⚠️  데이터베이스 연결 실패: {e}")
        print("\n.env 파일의 DATABASE_URL을 확인해주세요.")
        return
    
    # 테이블 생성
    print("\n[2단계] 테이블 생성 중...")
    try:
        init_db()
        print("✅ 테이블 생성 완료!")
    except Exception as e:
        print(f"❌ 테이블 생성 실패: {e}")
        return
    
    # 생성된 테이블 확인
    print("\n[3단계] 생성된 테이블 확인...")
    try:
        new_tables = check_tables()
        print(f"생성된 테이블: {new_tables}")
        
        expected_tables = ['users', 'search_histories', 'categories']
        missing_tables = [t for t in expected_tables if t not in new_tables]
        
        if missing_tables:
            print(f"⚠️  누락된 테이블: {missing_tables}")
        else:
            print("✅ 모든 테이블이 정상적으로 생성되었습니다!")
    except Exception as e:
        print(f"⚠️  테이블 확인 실패: {e}")
    
    print("\n" + "=" * 50)
    print("마이그레이션 완료!")
    print("=" * 50)

if __name__ == "__main__":
    main()

