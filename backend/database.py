"""
데이터베이스 연결 설정
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# 데이터베이스 URL
# 로컬: mysql+pymysql://user:password@localhost:3306/briefly
# AWS RDS: mysql+pymysql://user:password@rds-endpoint:3306/briefly
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/briefly_db"
)

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 연결 확인
    pool_recycle=3600,   # 1시간마다 연결 재활용
    echo=False  # SQL 쿼리 로그 (개발 시 True로 변경 가능)
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()


def get_db():
    """
    데이터베이스 세션 의존성
    FastAPI에서 Depends()로 사용
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    데이터베이스 테이블 생성
    """
    from models import user_models  # noqa
    Base.metadata.create_all(bind=engine, checkfirst=True)

