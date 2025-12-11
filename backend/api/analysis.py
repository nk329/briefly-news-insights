"""
분석 API 라우터
키워드 분석, 워드클라우드 등
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from services.keyword_analyzer import analyze_articles_keywords, analyze_keywords
from services.wordcloud_generator import generate_wordcloud, cleanup_old_wordclouds

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


class WordCloudRequest(BaseModel):
    """워드클라우드 생성 요청"""
    keywords: Dict[str, int]  # {"단어": 빈도수}
    width: Optional[int] = 600
    height: Optional[int] = 400


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


@router.post("/wordcloud")
async def generate_wordcloud_api(request: WordCloudRequest):
    """워드클라우드 이미지 생성
    
    Args:
        request: 키워드 딕셔너리 및 옵션
        
    Returns:
        생성된 이미지 URL
    """
    try:
        logger.info(f"워드클라우드 생성 요청: {len(request.keywords)}개 키워드")
        
        # 오래된 이미지 정리 (24시간 이상)
        cleanup_old_wordclouds(max_age_hours=24)
        
        # 워드클라우드 생성
        image_url = generate_wordcloud(
            keywords=request.keywords,
            width=request.width,
            height=request.height
        )
        
        return {
            "status": "success",
            "data": {
                "imageUrl": image_url
            }
        }
        
    except Exception as e:
        logger.error(f"워드클라우드 생성 API 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"워드클라우드 생성 실패: {str(e)}"
        )


@router.post("/articles/complete")
async def complete_analysis_api(request: ArticlesKeywordRequest):
    """통합 분석 (키워드 + 워드클라우드)
    
    Args:
        request: 기사 리스트 및 옵션
        
    Returns:
        키워드 분석 결과 + 워드클라우드 이미지 URL
    """
    try:
        logger.info(f"통합 분석 요청: {len(request.articles)}개 기사")
        
        # 1. 키워드 분석
        result = analyze_articles_keywords(request.articles, request.top_n)
        
        # 2. 워드클라우드 생성 (키워드가 있을 때만)
        image_url = ""
        if result.get("keywords"):
            # 키워드를 딕셔너리로 변환
            keywords_dict = {
                item["word"]: item["count"]
                for item in result["keywords"]
            }
            
            # 오래된 이미지 정리
            cleanup_old_wordclouds(max_age_hours=24)
            
            # 워드클라우드 생성
            image_url = generate_wordcloud(keywords=keywords_dict)
        
        return {
            "status": "success",
            "data": {
                **result,
                "wordcloudUrl": image_url
            }
        }
        
    except Exception as e:
        logger.error(f"통합 분석 API 에러: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"통합 분석 실패: {str(e)}"
        )

