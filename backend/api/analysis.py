"""
분석 API 라우터
키워드 분석, 워드클라우드 등
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from services.keyword_analyzer import analyze_articles_keywords, analyze_keywords

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


class KeywordRequest(BaseModel):
    """키워드 분석 요청"""
    texts: List[str]
    top_n: Optional[int] = 20
    

class ArticlesKeywordRequest(BaseModel):
    """기사 키워드 분석 요청"""
    articles: List[dict]
    top_n: Optional[int] = 20


@router.post("/keywords")
async def analyze_keywords_api(request: KeywordRequest):
    """텍스트 리스트에서 키워드 분석
    
    Args:
        request: 텍스트 리스트 및 옵션
        
    Returns:
        키워드 분석 결과
    """
    try:
        logger.info(f"키워드 분석 요청: {len(request.texts)}개 텍스트")
        
        keywords = analyze_keywords(request.texts, request.top_n)
        
        return {
            "status": "success",
            "data": {
                "keywords": keywords,
                "total": len(keywords)
            }
        }
        
    except Exception as e:
        logger.error(f"키워드 분석 API 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"키워드 분석 실패: {str(e)}"
        )


@router.post("/articles/keywords")
async def analyze_articles_keywords_api(request: ArticlesKeywordRequest):
    """뉴스 기사에서 키워드 분석
    
    Args:
        request: 기사 리스트 및 옵션
        
    Returns:
        키워드 분석 결과
    """
    try:
        logger.info(f"기사 키워드 분석 요청: {len(request.articles)}개 기사")
        
        result = analyze_articles_keywords(request.articles, request.top_n)
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"기사 키워드 분석 API 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"기사 키워드 분석 실패: {str(e)}"
        )

