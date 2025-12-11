from fastapi import APIRouter, Query, HTTPException
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
import logging
from services.summarizer import summarize_articles

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

# API 키 확인
api_key = os.getenv("NEWS_API_KEY")
logger.info(f"API Key 로드됨: {'있음' if api_key else '없음'}")
if api_key:
    logger.info(f"API Key 길이: {len(api_key)}")

router = APIRouter(prefix="/api/news", tags=["news"])
newsapi = NewsApiClient(api_key=api_key)

@router.get("/search")
async def search_news(
    keyword: str = Query(..., description="검색 키워드"),
    from_date: str = Query(None, description="시작일 (YYYY-MM-DD)"),
    to_date: str = Query(None, description="종료일 (YYYY-MM-DD)"),
    page_size: int = Query(10, ge=1, le=100, description="결과 개수"),
    summarize: bool = Query(True, description="요약 포함 여부")
):
    """뉴스 검색 및 요약 API
    
    Args:
        keyword: 검색할 키워드
        from_date: 검색 시작일
        to_date: 검색 종료일
        page_size: 결과 개수 (1-100)
        summarize: 요약 포함 여부 (기본 True)
    
    Returns:
        뉴스 기사 목록 (요약 포함)
    """
    try:
        logger.info(f"뉴스 검색 시작: keyword={keyword}, from={from_date}, to={to_date}")
        
        # NewsAPI get_everything은 language 파라미터 제한적
        # 한국어 뉴스는 키워드에 한글 포함 시 자동 검색됨
        response = newsapi.get_everything(
            q=keyword,
            from_param=from_date,
            to=to_date,
            sort_by='publishedAt',
            page_size=page_size
        )
        
        logger.info(f"검색 성공: {response['totalResults']}건")
        
        articles = response['articles']
        
        # 요약 기능 적용
        if summarize and articles:
            logger.info(f"요약 시작: {len(articles)}개 기사")
            articles = summarize_articles(articles, num_sentences=3)
            logger.info("요약 완료")
        
        return {
            "status": "success",
            "data": {
                "total": response['totalResults'],
                "articles": articles
            }
        }
    except Exception as e:
        logger.error(f"뉴스 검색 에러: {type(e).__name__}: {str(e)}")
        logger.exception("상세 에러:")
        raise HTTPException(status_code=500, detail=f"뉴스 검색 실패: {str(e)}")