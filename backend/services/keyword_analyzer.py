"""
키워드 분석 서비스
KoNLPy를 사용한 한글 형태소 분석 및 키워드 추출
"""

from konlpy.tag import Okt
from collections import Counter
import logging
import re

logger = logging.getLogger(__name__)

# 형태소 분석기 초기화 (전역으로 한 번만)
try:
    okt = Okt()
    logger.info("KoNLPy Okt 형태소 분석기 초기화 완료")
except Exception as e:
    logger.error(f"KoNLPy 초기화 실패: {e}")
    okt = None


# 한글 불용어 리스트
STOPWORDS = {
    # 조사, 접속사
    '것', '등', '수', '때', '년', '월', '일', '곳', '중', '내', '외',
    # 대명사
    '이', '그', '저', '이것', '그것', '저것', '여기', '거기', '저기',
    # 일반 단어
    '있다', '없다', '하다', '되다', '이다', '아니다',
    '통해', '위해', '대해', '따라', '의해', '관련', '현재', '최근',
    '우리', '저희', '기자', '뉴스', '오늘', '어제', '내일',
    '지난', '다음', '올해', '작년', '내년', '이번', '지난해',
    # 기타
    '때문', '경우', '정도', '만큼', '이상', '이하', '약', '전', '후',
}


def clean_text(text: str) -> str:
    """텍스트 정제
    
    Args:
        text: 원본 텍스트
        
    Returns:
        정제된 텍스트
    """
    if not text:
        return ""
    
    # URL 제거
    text = re.sub(r'http[s]?://\S+', '', text)
    # 이메일 제거
    text = re.sub(r'\S+@\S+', '', text)
    # 특수문자 제거 (한글, 영문, 숫자, 공백만 남김)
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', text)
    # 연속 공백 제거
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def extract_keywords(text: str, top_n: int = 20, min_length: int = 2) -> list:
    """단일 텍스트에서 키워드 추출
    
    Args:
        text: 분석할 텍스트
        top_n: 추출할 키워드 개수
        min_length: 최소 단어 길이
        
    Returns:
        키워드 리스트 [{"word": "단어", "count": 빈도}]
    """
    if not okt:
        logger.error("KoNLPy가 초기화되지 않았습니다")
        return []
    
    try:
        # 텍스트 정제
        cleaned_text = clean_text(text)
        
        if not cleaned_text:
            return []
        
        # 명사 추출
        nouns = okt.nouns(cleaned_text)
        
        # 필터링
        filtered_nouns = [
            word for word in nouns
            if len(word) >= min_length  # 최소 길이
            and word not in STOPWORDS  # 불용어 제외
            and not word.isdigit()  # 숫자만 있는 단어 제외
        ]
        
        # 빈도 계산
        counter = Counter(filtered_nouns)
        
        # 상위 N개 추출
        keywords = [
            {"word": word, "count": count}
            for word, count in counter.most_common(top_n)
        ]
        
        logger.info(f"키워드 추출 완료: {len(keywords)}개")
        return keywords
        
    except Exception as e:
        logger.error(f"키워드 추출 중 에러: {type(e).__name__}: {e}")
        return []


def analyze_keywords(texts: list, top_n: int = 20, min_length: int = 2) -> list:
    """여러 텍스트에서 키워드 분석
    
    Args:
        texts: 텍스트 리스트
        top_n: 추출할 키워드 개수
        min_length: 최소 단어 길이
        
    Returns:
        키워드 리스트 [{"word": "단어", "count": 빈도}]
    """
    if not texts:
        logger.warning("분석할 텍스트가 없습니다")
        return []
    
    try:
        # 모든 텍스트 합치기
        combined_text = ' '.join([str(t) for t in texts if t])
        
        logger.info(f"키워드 분석 시작: {len(texts)}개 텍스트, 총 {len(combined_text)}자")
        
        # 키워드 추출
        keywords = extract_keywords(combined_text, top_n, min_length)
        
        return keywords
        
    except Exception as e:
        logger.error(f"키워드 분석 중 에러: {type(e).__name__}: {e}")
        logger.exception("상세 에러:")
        return []


def analyze_articles_keywords(articles: list, top_n: int = 20) -> dict:
    """뉴스 기사 리스트에서 키워드 분석
    
    Args:
        articles: 뉴스 기사 리스트
        top_n: 추출할 키워드 개수
        
    Returns:
        분석 결과 {"keywords": [...], "total_words": N}
    """
    try:
        # 모든 기사의 제목, 설명, 본문 수집
        texts = []
        for article in articles:
            # 제목 추가 (중요도 높음)
            if article.get('title'):
                texts.append(article['title'])
                texts.append(article['title'])  # 2번 추가 (가중치)
            
            # 설명 추가
            if article.get('description'):
                texts.append(article['description'])
            
            # 본문 추가
            if article.get('content'):
                # [+XXX chars] 제거
                content = re.sub(r'\[\+\d+ chars\]', '', article['content'])
                texts.append(content)
        
        logger.info(f"총 {len(texts)}개 텍스트 수집 ({len(articles)}개 기사)")
        
        # 키워드 분석
        keywords = analyze_keywords(texts, top_n)
        
        # 총 단어 수 계산
        total_words = sum(kw['count'] for kw in keywords)
        
        return {
            "keywords": keywords,
            "total_words": total_words,
            "analyzed_articles": len(articles)
        }
        
    except Exception as e:
        logger.error(f"기사 키워드 분석 중 에러: {e}")
        return {"keywords": [], "total_words": 0, "analyzed_articles": 0}




