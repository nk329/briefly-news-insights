"""
사용자 관련 Pydantic 스키마 (Request/Response)
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ==================== User Schemas ====================
class UserCreate(BaseModel):
    """회원가입 요청"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """로그인 요청"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """사용자 정보 응답"""
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT 토큰 응답"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ==================== SearchHistory Schemas ====================
class SearchHistoryCreate(BaseModel):
    """검색 히스토리 생성 요청"""
    keyword: str
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    results_count: int = 0


class SearchHistoryResponse(BaseModel):
    """검색 히스토리 응답"""
    id: int
    keyword: str
    from_date: Optional[str]
    to_date: Optional[str]
    results_count: int
    searched_at: datetime

    class Config:
        from_attributes = True


# ==================== Category Schemas ====================
class CategoryCreate(BaseModel):
    """카테고리 생성 요청"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    color: str = Field(default="#1976d2", pattern="^#[0-9A-Fa-f]{6}$")


class CategoryUpdate(BaseModel):
    """카테고리 수정 요청"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")


class CategoryResponse(BaseModel):
    """카테고리 응답"""
    id: int
    name: str
    description: Optional[str]
    color: str
    created_at: datetime

    class Config:
        from_attributes = True



