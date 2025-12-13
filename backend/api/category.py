"""
카테고리 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user_models import User, Category
from models.user_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    사용자의 카테고리 목록 조회
    """
    categories = db.query(Category)\
        .filter(Category.user_id == current_user.id)\
        .order_by(Category.created_at)\
        .all()
    
    return categories


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    새 카테고리 생성
    """
    # 카테고리 이름 중복 확인
    existing_category = db.query(Category)\
        .filter(
            Category.user_id == current_user.id,
            Category.name == category_data.name
        )\
        .first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 카테고리 이름입니다"
        )
    
    new_category = Category(
        user_id=current_user.id,
        name=category_data.name,
        description=category_data.description,
        color=category_data.color
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    카테고리 수정
    """
    category = db.query(Category)\
        .filter(
            Category.id == category_id,
            Category.user_id == current_user.id
        )\
        .first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="카테고리를 찾을 수 없습니다"
        )
    
    # 업데이트
    if category_data.name is not None:
        # 이름 중복 확인
        existing = db.query(Category)\
            .filter(
                Category.user_id == current_user.id,
                Category.name == category_data.name,
                Category.id != category_id
            )\
            .first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 카테고리 이름입니다"
            )
        
        category.name = category_data.name
    
    if category_data.description is not None:
        category.description = category_data.description
    
    if category_data.color is not None:
        category.color = category_data.color
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    카테고리 삭제
    """
    category = db.query(Category)\
        .filter(
            Category.id == category_id,
            Category.user_id == current_user.id
        )\
        .first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="카테고리를 찾을 수 없습니다"
        )
    
    db.delete(category)
    db.commit()
    
    return None

