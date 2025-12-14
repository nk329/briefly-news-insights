"""
로컬 MySQL에서 RDS로 데이터 마이그레이션 스크립트
"""
import sys
import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from models.user_models import User, SearchHistory, Category

load_dotenv()

def parse_database_url(url):
    """DATABASE_URL을 파싱하여 연결 정보 추출"""
    if "mysql+pymysql://" in url:
        url_part = url.replace("mysql+pymysql://", "")
        auth_part, rest = url_part.split("@", 1)
        user, password = auth_part.split(":", 1)
        
        if "/" in rest:
            host_port, database = rest.split("/", 1)
        else:
            host_port = rest
            database = None
        
        if ":" in host_port:
            host, port = host_port.split(":", 1)
            port = int(port)
        else:
            host = host_port
            port = 3306
        
        return {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }
    return None

def migrate_data():
    """로컬 MySQL에서 RDS로 데이터 마이그레이션"""
    print("=" * 50)
    print("데이터 마이그레이션 시작")
    print("=" * 50)
    print("")
    
    # 로컬 DATABASE_URL (기본값)
    local_url = "mysql+pymysql://root:1234@localhost:3306/briefly_db"
    local_info = parse_database_url(local_url)
    
    # RDS DATABASE_URL (.env에서 읽기)
    rds_url = os.getenv("DATABASE_URL")
    if not rds_url:
        print("❌ .env 파일에 DATABASE_URL이 없습니다.")
        return False
    
    rds_info = parse_database_url(rds_url)
    if not rds_info:
        print("❌ DATABASE_URL 형식이 올바르지 않습니다.")
        return False
    
    print("로컬 MySQL 정보:")
    print(f"  호스트: {local_info['host']}")
    print(f"  데이터베이스: {local_info['database']}")
    print("")
    print("RDS 정보:")
    print(f"  호스트: {rds_info['host']}")
    print(f"  데이터베이스: {rds_info['database']}")
    print("")
    
    # 확인
    confirm = input("위 정보가 맞나요? (Y/N): ")
    if confirm.lower() != 'y':
        print("취소되었습니다.")
        return False
    
    try:
        # 로컬 MySQL 연결
        print("\n[1단계] 로컬 MySQL에 연결 중...")
        local_engine = create_engine(local_url)
        LocalSession = sessionmaker(bind=local_engine)
        local_db = LocalSession()
        print("✅ 로컬 MySQL 연결 성공!")
        
        # RDS 연결
        print("\n[2단계] RDS에 연결 중...")
        rds_engine = create_engine(rds_url)
        RdsSession = sessionmaker(bind=rds_engine)
        rds_db = RdsSession()
        print("✅ RDS 연결 성공!")
        
        # 사용자 데이터 마이그레이션
        print("\n[3단계] 사용자 데이터 마이그레이션 중...")
        local_users = local_db.query(User).all()
        print(f"  로컬 사용자 수: {len(local_users)}")
        
        migrated_users = 0
        for user in local_users:
            # RDS에 이미 존재하는지 확인
            existing = rds_db.query(User).filter(User.email == user.email).first()
            if existing:
                print(f"  ⚠️  사용자 '{user.email}'는 이미 존재합니다. 건너뜁니다.")
                continue
            
            # 새 사용자 생성 (비밀번호는 그대로 복사)
            new_user = User(
                email=user.email,
                username=user.username,
                hashed_password=user.hashed_password,
                created_at=user.created_at
            )
            rds_db.add(new_user)
            migrated_users += 1
        
        rds_db.commit()
        print(f"  ✅ {migrated_users}명의 사용자 마이그레이션 완료!")
        
        # 검색 히스토리 마이그레이션
        print("\n[4단계] 검색 히스토리 마이그레이션 중...")
        local_histories = local_db.query(SearchHistory).all()
        print(f"  로컬 검색 히스토리 수: {len(local_histories)}")
        
        # 사용자 ID 매핑 (로컬 ID -> RDS ID)
        user_id_map = {}
        for user in local_users:
            rds_user = rds_db.query(User).filter(User.email == user.email).first()
            if rds_user:
                user_id_map[user.id] = rds_user.id
        
        migrated_histories = 0
        for history in local_histories:
            if history.user_id not in user_id_map:
                print(f"  ⚠️  사용자 ID {history.user_id}에 대한 매핑이 없습니다. 건너뜁니다.")
                continue
            
            new_history = SearchHistory(
                user_id=user_id_map[history.user_id],
                keyword=history.keyword,
                from_date=history.from_date,
                to_date=history.to_date,
                results_count=history.results_count,
                searched_at=history.searched_at
            )
            rds_db.add(new_history)
            migrated_histories += 1
        
        rds_db.commit()
        print(f"  ✅ {migrated_histories}개의 검색 히스토리 마이그레이션 완료!")
        
        # 카테고리 마이그레이션
        print("\n[5단계] 카테고리 마이그레이션 중...")
        local_categories = local_db.query(Category).all()
        print(f"  로컬 카테고리 수: {len(local_categories)}")
        
        migrated_categories = 0
        for category in local_categories:
            if category.user_id not in user_id_map:
                print(f"  ⚠️  사용자 ID {category.user_id}에 대한 매핑이 없습니다. 건너뜁니다.")
                continue
            
            new_category = Category(
                user_id=user_id_map[category.user_id],
                name=category.name,
                description=category.description,
                color=category.color,
                created_at=category.created_at
            )
            rds_db.add(new_category)
            migrated_categories += 1
        
        rds_db.commit()
        print(f"  ✅ {migrated_categories}개의 카테고리 마이그레이션 완료!")
        
        local_db.close()
        rds_db.close()
        
        print("\n" + "=" * 50)
        print("✅ 데이터 마이그레이션 완료!")
        print(f"  - 사용자: {migrated_users}명")
        print(f"  - 검색 히스토리: {migrated_histories}개")
        print(f"  - 카테고리: {migrated_categories}개")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    migrate_data()

