"""
경량 요약 서비스 (서버 안정화 버전)
- 외부 라이브러리(sklearn, numpy) 제거
- 요약은 간단히 description/content 앞부분을 잘라 반환
"""

import logging
import re

logger = logging.getLogger(__name__)


def summarize_text(text: str, num_sentences: int = 3) -> str:
    """간단 요약: 앞부분 자르기"""
    if not text:
        return ""
    # NewsAPI 메타데이터 제거
    text = re.sub(r"\\[\\+\\d+ chars\\]", "", text)
    # 최대 길이 제한 (약 400자)
    return text[:400]


def summarize_articles(articles: list, num_sentences: int = 3) -> list:
    """여러 기사를 요약 (경량 처리)"""
    for article in articles:
        text = article.get("content") or article.get("description") or ""
        article["summary"] = summarize_text(text, num_sentences)
        logger.debug(f"기사 요약 완료(경량): {article.get('title', '')[:50]}...")
    return articles







