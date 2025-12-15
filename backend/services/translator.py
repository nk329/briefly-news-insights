"""
뉴스 기사 번역 서비스

deep-translator를 사용하여 뉴스 제목과 설명을 한국어로 번역합니다.
GPT를 사용하여 검색 키워드를 국가별 언어로 번역합니다.
"""

from deep_translator import GoogleTranslator
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# GPT 클라이언트 (키워드 번역용)
try:
    from openai import OpenAI
    gpt_client = None
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your-openai-api-key-here":
        gpt_client = OpenAI(api_key=api_key)
        logger.info("GPT 클라이언트 초기화 성공 (키워드 번역용)")
    else:
        logger.warning("OPENAI_API_KEY가 없어 GPT 키워드 번역을 사용할 수 없습니다.")
except Exception as e:
    logger.warning(f"GPT 클라이언트 초기화 실패 (키워드 번역): {e}")
    gpt_client = None

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


def translate_text_with_gpt(text: str, target_lang: str = "ko", source_lang: str = "auto") -> str:
    """
    GPT를 사용하여 텍스트를 번역합니다. (더 정확한 번역)
    
    Args:
        text: 번역할 텍스트
        target_lang: 대상 언어 코드 (ko, en, ja 등)
        source_lang: 원본 언어 (auto로 자동 감지)
    
    Returns:
        번역된 텍스트 (실패 시 None 반환)
    """
    if not gpt_client or not text or not text.strip():
        return None
    
    if target_lang not in SUPPORTED_LANGUAGES:
        return None
    
    try:
        target_language_name = SUPPORTED_LANGUAGES.get(target_lang, target_lang)
        
        # 원본 언어 감지 (간단한 휴리스틱)
        detected_lang = source_lang
        if source_lang == "auto":
            # 간단한 언어 감지
            if any('\u4e00' <= c <= '\u9fff' for c in text[:100]):  # 중국어
                detected_lang = "중국어"
            elif any('가' <= c <= '힣' for c in text[:100]):  # 한국어
                detected_lang = "한국어"
            elif any('ぁ' <= c <= 'ん' or 'ァ' <= c <= 'ヴ' for c in text[:100]):  # 일본어
                detected_lang = "일본어"
            else:
                detected_lang = "자동 감지"
        
        logger.debug(f"GPT 번역 시도: {len(text)}자 → {target_language_name}")
        
        response = gpt_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"당신은 전문 번역가입니다. 주어진 텍스트를 {target_language_name}로 자연스럽고 정확하게 번역하세요.\n\n중요 규칙:\n- 원문의 의미를 정확히 전달하세요\n- 자연스러운 {target_language_name} 표현을 사용하세요\n- 전문 용어는 {target_language_name} 표준 용어로 번역하세요\n- 번역된 텍스트만 반환하세요 (설명 없이)"
                },
                {
                    "role": "user",
                    "content": f"다음 텍스트를 {target_language_name}로 번역하세요:\n\n{text[:3000]}"  # 최대 3000자
                }
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        
        translated = response.choices[0].message.content.strip()
        logger.debug(f"GPT 번역 성공: {len(text)}자 → {len(translated)}자")
        return translated
        
    except Exception as e:
        logger.warning(f"GPT 번역 실패: {e}")
        return None


def translate_text(text: str, target_lang: str = "ko", source_lang: str = "auto", use_gpt: bool = False) -> str:
    """
    텍스트를 지정된 언어로 번역합니다.
    GPT를 우선 사용하고, 실패 시 Google Translator로 폴백합니다.
    
    Args:
        text: 번역할 텍스트
        target_lang: 대상 언어 코드 (ko, en, ja 등)
        source_lang: 원본 언어 (auto로 자동 감지)
        use_gpt: GPT 사용 여부 (기본 True)
    
    Returns:
        번역된 텍스트
    """
    if not text or not text.strip():
        return text
    
    if target_lang not in SUPPORTED_LANGUAGES:
        logger.warning(f"지원하지 않는 언어: {target_lang}")
        return text
    
    # ⚠️ 서버 성능 및 타임아웃 이슈로 인해
    # 현재 프로덕션 환경에서는 GPT 번역을 비활성화합니다.
    # (필요 시 환경 변수로 다시 활성화하는 방식 권장)
    
    # Google Translator로 폴백
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text[:5000])  # 최대 5000자로 제한
        
        logger.debug(f"Google Translator 번역 완료: {len(text)}자 → {len(translated)}자")
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


def translate_keyword_for_country(keyword: str, country: str) -> str:
    """
    검색 키워드를 해당 국가의 언어로 번역합니다.
    GPT를 우선 사용하고, 실패 시 Google Translator로 폴백합니다.
    
    Args:
        keyword: 검색 키워드 (예: "비트코인")
        country: 국가 코드 (kr, us, jp, cn, fr, de 등)
    
    Returns:
        번역된 키워드 (예: "Bitcoin", "ビットコイン")
    """
    if not keyword or not keyword.strip():
        return keyword
    
    # 국가별 언어 매핑
    country_language_map = {
        "kr": "한국어",
        "us": "영어",
        "gb": "영어",
        "au": "영어",
        "ca": "영어",
        "jp": "일본어",
        "cn": "중국어",
        "fr": "프랑스어",
        "de": "독일어",
    }
    
    target_language = country_language_map.get(country)
    if not target_language:
        return keyword  # 매핑 없으면 원본 반환
    
    # GPT로 번역 시도 (더 정확함)
    if gpt_client:
        try:
            logger.info(f"GPT로 키워드 번역 시도: '{keyword}' → {target_language}")
            response = gpt_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": f"당신은 전문 번역가입니다. 주어진 검색 키워드를 {target_language}로 정확하게 번역하세요.\n\n중요 규칙:\n- {target_language}로만 번역하세요 (다른 언어나 OR 조건 사용 금지)\n- 일본어면 일본어로만, 영어면 영어로만, 중국어면 중국어로만\n- 전문 용어는 해당 언어의 표준 용어 사용\n- 번역된 키워드 하나만 반환하세요 (설명, 예시, OR 조건 없이)\n- 예: '비트코인' → 일본어면 'ビットコイン' (Bitcoin 아님, OR 없음)"
                    },
                    {
                        "role": "user",
                        "content": f"다음 검색 키워드를 {target_language}로만 번역하세요 (단일 키워드만 반환): {keyword}"
                    }
                ],
                temperature=0.2,  # 더 일관된 결과를 위해 낮춤
                max_tokens=30,  # 짧은 키워드만 반환
            )
            
            translated = response.choices[0].message.content.strip()
            
            # OR, "또는", "|" 같은 조건 제거 (혹시 모를 경우 대비)
            if " OR " in translated.upper() or " 또는 " in translated or "|" in translated:
                # 첫 번째 키워드만 사용
                translated = translated.split(" OR ")[0].split(" 또는 ")[0].split("|")[0].strip()
                logger.warning(f"OR 조건 제거: '{translated}'")
            
            # 따옴표 제거 (GPT가 따옴표로 감쌀 수 있음)
            translated = translated.strip('"').strip("'").strip()
            
            logger.info(f"GPT 키워드 번역 성공: '{keyword}' → '{translated}'")
            return translated
            
        except Exception as e:
            logger.warning(f"GPT 키워드 번역 실패: {e}, Google Translator로 폴백")
    
    # GPT 실패 시 Google Translator로 폴백
    try:
        # 국가 코드를 언어 코드로 변환
        country_lang_map = {
            "kr": "ko",
            "us": "en",
            "gb": "en",
            "au": "en",
            "ca": "en",
            "jp": "ja",
            "cn": "zh-CN",
            "fr": "fr",
            "de": "de",
        }
        
        target_lang_code = country_lang_map.get(country, "en")
        translator = GoogleTranslator(source='auto', target=target_lang_code)
        translated = translator.translate(keyword)
        
        # OR 조건 제거 (혹시 모를 경우 대비)
        if " OR " in translated.upper() or " 또는 " in translated or "|" in translated:
            translated = translated.split(" OR ")[0].split(" 또는 ")[0].split("|")[0].strip()
            logger.warning(f"Google Translator OR 조건 제거: '{translated}'")
        
        # 따옴표 제거
        translated = translated.strip('"').strip("'").strip()
        
        logger.info(f"Google Translator 키워드 번역: '{keyword}' → '{translated}'")
        return translated
        
    except Exception as e:
        logger.error(f"키워드 번역 실패: {e}")
        return keyword  # 실패 시 원본 반환


