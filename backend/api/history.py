"""
검색 히스토리 API 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user_models import User, SearchHistory
from models.user_schemas import SearchHistoryCreate, SearchHistoryResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("/", response_model=List[SearchHistoryResponse])
async def get_search_histories(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    사용자의 검색 히스토리 조회 (최신순)
    """
    histories = db.query(SearchHistory)\
        .filter(SearchHistory.user_id == current_user.id)\
        .order_by(SearchHistory.searched_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return histories


@router.post("/", response_model=SearchHistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_search_history(
    history_data: SearchHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    검색 히스토리 저장
    """
    new_history = SearchHistory(
        user_id=current_user.id,
        keyword=history_data.keyword,
        from_date=history_data.from_date,
        to_date=history_data.to_date,
        results_count=history_data.results_count
    )
    
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    
    return new_history


@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_search_history(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    검색 히스토리 삭제
    """
    history = db.query(SearchHistory)\
        .filter(
            SearchHistory.id == history_id,
            SearchHistory.user_id == current_user.id
        )\
        .first()
    
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="검색 히스토리를 찾을 수 없습니다"
        )
    
    db.delete(history)
    db.commit()
    
    return None


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_search_histories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    사용자의 모든 검색 히스토리 삭제
    """
    db.query(SearchHistory)\
        .filter(SearchHistory.user_id == current_user.id)\
        .delete()
    
    db.commit()
    
    return None



