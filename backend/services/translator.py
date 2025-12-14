"""
뉴스 기사 번역 서비스

deep-translator를 사용하여 뉴스 제목과 설명을 한국어로 번역합니다.
"""

from deep_translator import GoogleTranslator
import logging

logger = logging.getLogger(__name__)

# 지원 언어
SUPPORTED_LANGUAGES = {
    "ko": "Korean",
    "en": "English",
    "ja": "Japanese",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ar": "Arabic"
}


def translate_text(text: str, target_lang: str = "ko", source_lang: str = "auto") -> str:
    """
    텍스트를 지정된 언어로 번역합니다.
    
    Args:
        text: 번역할 텍스트
        target_lang: 대상 언어 코드 (ko, en, ja 등)
        source_lang: 원본 언어 (auto로 자동 감지)
    
    Returns:
        번역된 텍스트
    """
    if not text or not text.strip():
        return text
    
    if target_lang not in SUPPORTED_LANGUAGES:
        logger.warning(f"지원하지 않는 언어: {target_lang}")
        return text
    
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text[:5000])  # 최대 5000자로 제한
        
        logger.debug(f"번역 완료: {len(text)}자 → {len(translated)}자")
        return translated
        
    except Exception as e:
        logger.error(f"번역 실패: {e}")
        return text  # 실패 시 원문 반환


def translate_articles(
    articles: list[dict],
    target_lang: str = "ko",
    translate_fields: list[str] = ["title", "description"]
) -> list[dict]:
    """
    뉴스 기사 목록을 번역합니다.
    
    Args:
        articles: 뉴스 기사 목록
        target_lang: 대상 언어 코드
        translate_fields: 번역할 필드 목록 (title, description 등)
    
    Returns:
        번역된 기사 목록 (translated_title, translated_description 필드 추가)
    """
    if not articles:
        return articles
    
    logger.info(f"{len(articles)}개 기사 번역 시작 (대상 언어: {target_lang})")
    
    translated_articles = []
    success_count = 0
    
    for idx, article in enumerate(articles):
        try:
            article_copy = {**article}
            
            # 제목 번역
            if "title" in translate_fields and article.get("title"):
                original_title = article.get("title", "")
                translated_title = translate_text(original_title, target_lang)
                article_copy["translated_title"] = translated_title
                article_copy["original_title"] = original_title
            
            # 설명 번역
            if "description" in translate_fields and article.get("description"):
                original_description = article.get("description", "")
                translated_description = translate_text(original_description, target_lang)
                article_copy["translated_description"] = translated_description
                article_copy["original_description"] = original_description
            
            # 번역 언어 정보 추가
            article_copy["translation_language"] = target_lang
            
            translated_articles.append(article_copy)
            success_count += 1
            
            logger.debug(f"기사 {idx+1}/{len(articles)} 번역 완료")
            
        except Exception as e:
            logger.error(f"기사 {idx+1} 번역 실패: {e}")
            # 번역 실패 시 원본 기사 그대로 추가
            translated_articles.append(article)
    
    logger.info(f"번역 완료: {success_count}/{len(articles)}개 성공")
    
    return translated_articles


def get_supported_languages() -> dict:
    """
    지원하는 언어 목록을 반환합니다.
    
    Returns:
        언어 코드: 언어명 딕셔너리
    """
    return SUPPORTED_LANGUAGES


def detect_language(text: str) -> str:
    """
    텍스트의 언어를 자동 감지합니다.
    
    Args:
        text: 분석할 텍스트
    
    Returns:
        감지된 언어 코드 (예: 'en', 'ko', 'ja')
    """
    if not text or not text.strip():
        return "unknown"
    
    try:
        # deep-translator는 자동 감지를 지원하지 않으므로 
        # 간단한 휴리스틱 사용
        # (또는 langdetect 같은 라이브러리 추가 가능)
        
        # 한글 감지
        korean_chars = sum(1 for c in text if '가' <= c <= '힣')
        if korean_chars > len(text) * 0.3:
            return "ko"
        
        # 일본어 감지 (히라가나, 가타카나)
        japanese_chars = sum(1 for c in text if 
            ('ぁ' <= c <= 'ん') or ('ァ' <= c <= 'ヴ'))
        if japanese_chars > len(text) * 0.3:
            return "ja"
        
        # 중국어 감지
        chinese_chars = sum(1 for c in text if 
            '\u4e00' <= c <= '\u9fff')
        if chinese_chars > len(text) * 0.3:
            return "zh-CN"
        
        # 기본: 영어
        return "en"
        
    except Exception as e:
        logger.error(f"언어 감지 실패: {e}")
        return "unknown"


