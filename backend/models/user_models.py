"""
사용자 관련 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """사용자 모델"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계
    search_histories = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")


class SearchHistory(Base):
    """검색 히스토리 모델"""
    __tablename__ = "search_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    keyword = Column(String(255), nullable=False)
    from_date = Column(String(50))
    to_date = Column(String(50))
    results_count = Column(Integer, default=0)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계
    user = relationship("User", back_populates="search_histories")


class Category(Base):
    """사용자 카테고리 모델"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    color = Column(String(20), default="#1976d2")  # 카테고리 색상 (HEX)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계
    user = relationship("User", back_populates="categories")

