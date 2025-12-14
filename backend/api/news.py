from fastapi import APIRouter, Query, HTTPException
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
import logging
from services.summarizer import summarize_articles
from services.gpt_summarizer import summarize_articles_with_gpt
from services.translator import translate_articles

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
    keyword: str = Query(None, description="검색 키워드 (선택, 없으면 국가 헤드라인)"),
    country: str = Query("kr", description="국가 코드 (kr, us, jp, cn, gb, all 등)"),
    translate_to: str = Query("ko", description="번역 언어 (ko, en, ja, none)"),
    from_date: str = Query(None, description="시작일 (YYYY-MM-DD, all 모드에서만)"),
    to_date: str = Query(None, description="종료일 (YYYY-MM-DD, all 모드에서만)"),
    page_size: int = Query(5, ge=1, le=100, description="결과 개수"),
    use_gpt: bool = Query(False, description="GPT-4 요약 사용 여부")
):
    """국가별 뉴스 검색 및 번역 API
    
    Args:
        keyword: 검색 키워드 (없으면 해당 국가 헤드라인)
        country: 국가 코드 (kr, us, jp, cn, gb, all)
        translate_to: 번역 대상 언어 (ko, en, ja, none=번역안함)
        from_date: 시작일 (all 모드에서만 사용)
        to_date: 종료일 (all 모드에서만 사용)
        page_size: 결과 개수
        use_gpt: GPT-4 요약 사용 여부
    
    Returns:
        뉴스 기사 목록 (번역 및 요약 포함)
    """
    try:
        logger.info(f"뉴스 검색: country={country}, keyword={keyword}, translate={translate_to}")
        
        # 1. 뉴스 검색 (국가별 또는 전체)
        # NewsAPI 제한: 일부 국가(jp, cn 등)는 get_top_headlines에서 뉴스가 없을 수 있음
        # → 키워드가 있거나, 국가가 특정 국가면 get_everything 사용
        
        # 국가별 기본 키워드 (키워드가 없을 때 사용)
        country_keywords = {
            "jp": "日本 OR ニュース OR Japan",
            "cn": "中国 OR 新闻 OR China", 
            "kr": "한국 OR 뉴스 OR Korea",
            "us": "United States OR America",
            "gb": "United Kingdom OR Britain",
            "fr": "France OR français",
            "de": "Germany OR Deutschland",
            "au": "Australia",
            "ca": "Canada"
        }
        
        if country and country != "all":
            # 키워드가 있으면 그대로 사용, 없으면 국가별 기본 키워드 사용
            search_query = keyword if keyword else country_keywords.get(country, "news")
            
            # 먼저 get_top_headlines 시도 (일부 국가만 지원)
            logger.info(f"get_top_headlines 시도: country={country}, keyword={keyword or '없음'}")
            try:
                if keyword:
                    # 키워드가 있으면 get_everything 사용 (더 많은 결과)
                    response = newsapi.get_everything(
                        q=search_query,
                        from_param=from_date,
                        to=to_date,
                        sort_by='publishedAt',
                        page_size=page_size
                    )
                else:
                    # 키워드 없으면 get_top_headlines 시도
                    response = newsapi.get_top_headlines(
                        country=country,
                        page_size=page_size
                    )
                    
                    # 결과가 없으면 get_everything으로 폴백
                    if response.get('totalResults', 0) == 0:
                        logger.info(f"get_top_headlines 결과 없음, get_everything으로 폴백")
                        response = newsapi.get_everything(
                            q=search_query,
                            sort_by='publishedAt',
                            page_size=page_size
                        )
            except Exception as e:
                # get_top_headlines 실패 시 get_everything으로 폴백
                logger.warning(f"get_top_headlines 실패: {e}, get_everything으로 폴백")
                response = newsapi.get_everything(
                    q=search_query,
                    sort_by='publishedAt',
                    page_size=page_size
                )
        else:
            # 전체 검색 (날짜 범위 가능)
            logger.info(f"get_everything 사용 (all 모드)")
            response = newsapi.get_everything(
                q=keyword if keyword else "news",
                from_param=from_date,
                to=to_date,
                sort_by='publishedAt',
                page_size=page_size
            )
        
        logger.info(f"검색 성공: {response.get('totalResults', 0)}건")
        
        articles = response.get('articles', [])
        
        # 결과가 없으면 에러 메시지 개선
        if not articles or len(articles) == 0:
            logger.warning(f"검색 결과 없음: country={country}, keyword={keyword}")
            return {
                "status": "success",
                "data": {
                    "total": 0,
                    "articles": [],
                    "country": country,
                    "translation_language": translate_to if translate_to != "none" else None,
                    "message": f"{country} 국가의 뉴스를 찾을 수 없습니다. 키워드를 입력해보세요."
                }
            }
        
        # 2. 번역 (translate_to가 "none"이 아닌 경우)
        if articles and translate_to and translate_to != "none":
            logger.info(f"번역 시작: {len(articles)}개 기사 → {translate_to}")
            try:
                articles = translate_articles(articles, target_lang=translate_to)
                logger.info("번역 완료")
            except Exception as translate_error:
                logger.error(f"번역 실패: {translate_error}")
                # 번역 실패 시 원문 그대로
        
        # 3. GPT 요약 (선택적)
        if use_gpt and articles:
            logger.info(f"GPT-4 요약 시작: {len(articles)}개 기사")
            try:
                articles = summarize_articles_with_gpt(articles, max_sentences=3)
                logger.info(f"GPT-4 요약 완료: {len(articles)}개 기사 처리됨")
                # 요약이 성공한 기사 수 확인
                summarized_count = sum(1 for a in articles if a.get('summary') and a.get('summary_type') == 'gpt')
                logger.info(f"GPT 요약 성공: {summarized_count}/{len(articles)}개")
            except Exception as gpt_error:
                logger.error(f"GPT-4 요약 실패: {gpt_error}")
                logger.exception("GPT 요약 상세 에러:")
                # GPT 요약 실패 시 원본 기사 그대로 반환 (summary 필드 없이)
                articles = [
                    {**article, "summary": None, "summary_type": "none"}
                    for article in articles
                ]
        else:
            logger.info("GPT 요약 비활성화")
        
        return {
            "status": "success",
            "data": {
                "total": response['totalResults'],
                "articles": articles,
                "country": country,
                "translation_language": translate_to if translate_to != "none" else None
            }
        }
    except Exception as e:
        logger.error(f"뉴스 검색 에러: {type(e).__name__}: {str(e)}")
        logger.exception("상세 에러:")
        raise HTTPException(status_code=500, detail=f"뉴스 검색 실패: {str(e)}")