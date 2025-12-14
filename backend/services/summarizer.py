"""
텍스트 요약 서비스
TF-IDF 기반 핵심 문장 추출
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
import logging

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """텍스트 전처리
    
    Args:
        text: 원본 텍스트
        
    Returns:
        정제된 텍스트
    """
    if not text:
        return ""
    
    # 특수문자, 이상한 공백 제거
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def split_sentences(text: str) -> list:
    """문장 분리
    
    Args:
        text: 전체 텍스트
        
    Returns:
        문장 리스트
    """
    # 문장 종결 부호로 분리
    sentences = re.split(r'[.!?]\s+', text)
    # 빈 문장 제거 및 정리
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def summarize_text(text: str, num_sentences: int = 3) -> str:
    """TF-IDF 기반 문장 추출 요약
    
    Args:
        text: 요약할 텍스트
        num_sentences: 추출할 문장 수 (기본 3)
        
    Returns:
        요약된 텍스트
    """
    try:
        # 텍스트 정제
        text = clean_text(text)
        
        if not text:
            logger.warning("요약할 텍스트가 없음")
            return ""
        
        # 문장 분리
        sentences = split_sentences(text)
        
        # 문장이 너무 적으면 그대로 반환
        if len(sentences) <= num_sentences:
            logger.info(f"문장 수({len(sentences)})가 적어 원문 반환")
            return text
        
        # TF-IDF 벡터화
        try:
            vectorizer = TfidfVectorizer(max_features=100)
            tfidf_matrix = vectorizer.fit_transform(sentences)
        except Exception as e:
            logger.error(f"TF-IDF 벡터화 실패: {e}")
            # 벡터화 실패 시 앞 문장들 반환
            return '. '.join(sentences[:num_sentences]) + '.'
        
        # 각 문장의 중요도 계산 (TF-IDF 벡터의 합)
        sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
        
        # 중요도 높은 문장 인덱스 추출
        top_indices = sentence_scores.argsort()[-num_sentences:][::-1]
        
        # 원본 순서대로 정렬
        top_indices_sorted = sorted(top_indices)
        
        # 선택된 문장들로 요약 생성
        summary_sentences = [sentences[i] for i in top_indices_sorted]
        summary = '. '.join(summary_sentences)
        
        # 마지막에 마침표가 없으면 추가
        if not summary.endswith('.'):
            summary += '.'
        
        logger.info(f"요약 완료: {len(sentences)}문장 → {num_sentences}문장")
        return summary
        
    except Exception as e:
        logger.error(f"요약 중 에러 발생: {type(e).__name__}: {e}")
        # 에러 시 원문의 앞부분 반환
        sentences = split_sentences(text)
        if sentences:
            return '. '.join(sentences[:num_sentences]) + '.'
        return text[:500] + '...' if len(text) > 500 else text


def summarize_articles(articles: list, num_sentences: int = 3) -> list:
    """여러 기사를 요약
    
    Args:
        articles: 기사 리스트
        num_sentences: 각 기사당 요약 문장 수
        
    Returns:
        요약이 추가된 기사 리스트
    """
    for article in articles:
        # content 또는 description 사용
        text = article.get('content') or article.get('description') or ''
        
        # [+XXX chars] 같은 NewsAPI 메타데이터 제거
        text = re.sub(r'\[\+\d+ chars\]', '', text)
        
        # 요약 생성
        if text:
            article['summary'] = summarize_text(text, num_sentences)
        else:
            article['summary'] = article.get('description', '')[:200]
        
        logger.debug(f"기사 요약 완료: {article.get('title', '')[:50]}...")
    
    return articles





