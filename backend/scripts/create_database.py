"""
RDS에 데이터베이스를 생성하는 스크립트
"""
import sys
import os
import pymysql

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

def create_database():
    """데이터베이스 생성"""
    # .env에서 DATABASE_URL 파싱
    database_url = os.getenv("DATABASE_URL", "")
    
    if not database_url:
        print("❌ DATABASE_URL이 .env 파일에 없습니다.")
        return False
    
    # DATABASE_URL 파싱: mysql+pymysql://user:password@host:port/database
    # 먼저 데이터베이스명을 제거하고 연결
    if "mysql+pymysql://" in database_url:
        url_part = database_url.replace("mysql+pymysql://", "")
        # user:password@host:port/database 형식
        if "@" in url_part:
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
            
            print(f"연결 정보:")
            print(f"  호스트: {host}")
            print(f"  포트: {port}")
            print(f"  사용자: {user}")
            print(f"  데이터베이스: {database}")
            print("")
            
            try:
                # 데이터베이스 없이 연결 (MySQL 서버에 직접 연결)
                print("[1단계] MySQL 서버에 연결 중...")
                connection = pymysql.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    charset='utf8mb4'
                )
                print("✅ 연결 성공!")
                
                # 데이터베이스 생성
                print(f"\n[2단계] 데이터베이스 '{database}' 생성 중...")
                with connection.cursor() as cursor:
                    # 데이터베이스가 이미 존재하는지 확인
                    cursor.execute("SHOW DATABASES LIKE %s", (database,))
                    exists = cursor.fetchone()
                    
                    if exists:
                        print(f"⚠️  데이터베이스 '{database}'가 이미 존재합니다.")
                        print("기존 데이터베이스를 사용합니다.")
                        # SSH 환경에서는 자동으로 기존 DB 사용
                    else:
                        # UTF8MB4로 데이터베이스 생성
                        cursor.execute(f"CREATE DATABASE `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                        connection.commit()
                        print(f"✅ 데이터베이스 '{database}' 생성 완료!")
                
                connection.close()
                return True
                
            except Exception as e:
                print(f"❌ 오류 발생: {e}")
                return False
        else:
            print("❌ DATABASE_URL 형식이 올바르지 않습니다.")
            return False
    else:
        print("❌ DATABASE_URL 형식이 올바르지 않습니다.")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("RDS 데이터베이스 생성 스크립트")
    print("=" * 50)
    print("")
    
    if create_database():
        print("\n" + "=" * 50)
        print("✅ 데이터베이스 생성 완료!")
        print("다음 단계: python scripts\\migrate_db.py 실행")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 데이터베이스 생성 실패")
        print("=" * 50)

