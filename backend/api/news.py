from fastapi import APIRouter, Query, HTTPException
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
import logging
import re
from services.summarizer import summarize_articles
from services.gpt_summarizer import summarize_articles_with_gpt
from services.translator import translate_articles, translate_keyword_for_country

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

# 언어별 필터링용 정규식
HANGUL_REGEX = re.compile(r"[가-힣]")  # 한국어
JAPANESE_REGEX = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]")  # 일본어 (히라가나, 가타카나, 한자)
CHINESE_REGEX = re.compile(r"[\u4E00-\u9FAF]")  # 중국어 (한자)
ENGLISH_REGEX = re.compile(r"[a-zA-Z]")  # 영어
FRENCH_REGEX = re.compile(r"[a-zA-Zàâäéèêëïîôùûüÿç]")  # 프랑스어
GERMAN_REGEX = re.compile(r"[a-zA-Zäöüß]")  # 독일어

# 국가별 언어 매핑
COUNTRY_LANGUAGE_REGEX = {
    "kr": HANGUL_REGEX,
    "jp": JAPANESE_REGEX,
    "cn": CHINESE_REGEX,
    "us": ENGLISH_REGEX,
    "gb": ENGLISH_REGEX,
    "au": ENGLISH_REGEX,
    "ca": ENGLISH_REGEX,
    "fr": FRENCH_REGEX,
    "de": GERMAN_REGEX,
}

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
            "jp": "ニュース OR Japan",
            "cn": "新闻 OR China",
            "kr": "뉴스 OR Korea",
            "us": "news OR United States OR America",
            "gb": "news OR United Kingdom OR Britain",
            "fr": "actualité OR France",
            "de": "Nachrichten OR Germany",
            "au": "news OR Australia",
            "ca": "news OR Canada",
        }
        
        # 국가별 대표 언론 도메인 (NewsAPI가 지원하는 도메인 위주, 예시는 확장 가능)
        country_domain_map: dict[str, list[str]] = {
            # 일본 주요 매체
            "jp": [
                "nhk.or.jp",
                "asahi.com",
                "yomiuri.co.jp",
                "mainichi.jp",
                "nikkei.com",
            ],
            # 중국 / 홍콩 매체 (NewsAPI에서 지원하는 일부 영어권 매체 포함)
            "cn": [
                "scmp.com",
                "globaltimes.cn",
            ],
            # 한국: NewsAPI에서 공식 지원은 제한적이지만, 확장 가능성을 고려해 정의
            "kr": [
                "yna.co.kr",
                "koreatimes.co.kr",
                "koreaherald.com",
            ],
            # 미국
            "us": [
                "nytimes.com",
                "wsj.com",
                "washingtonpost.com",
                "cnn.com",
                "foxnews.com",
                "nbcnews.com",
            ],
            # 영국
            "gb": [
                "bbc.co.uk",
                "theguardian.com",
                "independent.co.uk",
                "telegraph.co.uk",
            ],
            # 프랑스
            "fr": [
                "lemonde.fr",
                "lefigaro.fr",
            ],
            # 독일
            "de": [
                "spiegel.de",
                "faz.net",
            ],
            # 호주
            "au": [
                "abc.net.au",
                "theaustralian.com.au",
            ],
            # 캐나다
            "ca": [
                "theglobeandmail.com",
                "nationalpost.com",
            ],
        }
        
        # 모든 국가에서 도메인 필터링 제거 (언어 기반 필터링으로 대체)
        domains = None
        
        if country and country != "all":
            # 키워드가 있으면 해당 국가의 언어로 번역
            if keyword:
                logger.info(f"키워드 번역 시작: '{keyword}' (국가: {country})")
                translated_keyword = translate_keyword_for_country(keyword, country)
                logger.info(f"키워드 번역 완료: '{keyword}' → '{translated_keyword}'")
                search_query = translated_keyword
                logger.info(f"번역된 키워드로 검색: '{search_query}' (국가: {country})")
            else:
                # 키워드 없으면 국가별 기본 키워드 사용
                search_query = country_keywords.get(country, "news")
            
            # 도메인 필터링 없이 검색 (언어 기반 후처리 필터링 사용)
            logger.info(f"get_everything 사용: country={country}, from={from_date}, to={to_date} (도메인 필터링 없음)")
            # 인기 뉴스에 가깝게 가져오기 위해 popularity 기준으로 정렬
            response = newsapi.get_everything(
                q=search_query,
                from_param=from_date,
                to=to_date,
                sort_by="popularity",
                page_size=page_size,
            )
        else:
            # 전체 검색 (날짜 범위 가능)
            logger.info(f"get_everything 사용 (all 모드)")
            # 전체(all) 모드도 popularity 기준 정렬 사용
            response = newsapi.get_everything(
                q=keyword if keyword else "news",
                from_param=from_date,
                to=to_date,
                sort_by="popularity",
                page_size=page_size,
            )
        
        logger.info(f"검색 성공: {response.get('totalResults', 0)}건")
        
        articles = response.get('articles', [])

        # 국가별 언어 기반 기사 필터링
        if country and country != "all" and articles:
            language_regex = COUNTRY_LANGUAGE_REGEX.get(country)
            if language_regex:
                original_count = len(articles)
                filtered_articles = []
                for article in articles:
                    title = article.get("title", "") or ""
                    description = article.get("description", "") or ""
                    text = f"{title} {description}"
                    if language_regex.search(text):
                        filtered_articles.append(article)

                if filtered_articles:
                    logger.info(f"{country} 국가 언어 기사 필터링: {len(filtered_articles)}/{original_count}개 유지")
                    articles = filtered_articles
                else:
                    logger.info(f"{country} 국가 언어 기사를 찾지 못해 원본 결과를 그대로 사용합니다.")
        
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