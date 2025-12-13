"""
GPT-4 기반 뉴스 요약 서비스

OpenAI GPT-4o-mini를 사용하여 뉴스 기사를 자연스럽게 요약합니다.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# OpenAI 클라이언트 초기화
client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your-openai-api-key-here":
        client = OpenAI(api_key=api_key)
        logger.info("OpenAI 클라이언트 초기화 성공")
    else:
        logger.warning("OPENAI_API_KEY가 설정되지 않았습니다. GPT 요약을 사용할 수 없습니다.")
except Exception as e:
    logger.error(f"OpenAI 클라이언트 초기화 실패: {e}")


def summarize_with_gpt(
    text: str,
    max_sentences: int = 3,
    model: str = "gpt-4o-mini"
) -> str:
    """
    GPT-4를 사용하여 텍스트를 요약합니다.
    
    Args:
        text: 요약할 텍스트
        max_sentences: 최대 문장 수 (기본 3문장)
        model: 사용할 GPT 모델 (기본 gpt-4o-mini)
    
    Returns:
        요약된 텍스트
    
    Raises:
        Exception: API 키가 없거나 요청 실패 시
    """
    if not client:
        raise Exception("OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 추가하세요.")
    
    if not text or len(text.strip()) < 50:
        return text  # 텍스트가 너무 짧으면 그대로 반환
    
    try:
        # GPT-4에게 요약 요청
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"""당신은 뉴스 기사 요약 전문가입니다. 
주어진 뉴스 기사를 핵심 내용만 담아 {max_sentences}문장 이내로 간결하게 요약하세요.
- 객관적이고 중립적인 톤 유지
- 중요한 사실과 숫자 포함
- 불필요한 수식어 제거
- 한국어로 답변"""
                },
                {
                    "role": "user",
                    "content": f"다음 뉴스 기사를 {max_sentences}문장으로 요약하세요:\n\n{text}"
                }
            ],
            max_tokens=300,
            temperature=0.3,  # 일관된 요약을 위해 낮은 temperature
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        summary = response.choices[0].message.content.strip()
        
        logger.info(f"GPT 요약 성공 (모델: {model}, 원본: {len(text)}자 → 요약: {len(summary)}자)")
        
        return summary
    
    except Exception as e:
        logger.error(f"GPT 요약 실패: {e}")
        raise Exception(f"GPT 요약 중 오류 발생: {str(e)}")


def summarize_articles_with_gpt(
    articles: list[dict],
    max_sentences: int = 3,
    model: str = "gpt-4o-mini"
) -> list[dict]:
    """
    여러 뉴스 기사를 GPT로 요약합니다.
    
    Args:
        articles: 뉴스 기사 목록 (각 기사는 title, description, content 포함)
        max_sentences: 각 요약의 최대 문장 수
        model: 사용할 GPT 모델
    
    Returns:
        요약이 추가된 기사 목록 (gpt_summary 필드 추가)
    """
    if not client:
        logger.warning("OpenAI API 키가 없어 GPT 요약을 건너뜁니다.")
        return articles
    
    summarized_articles = []
    
    for article in articles:
        try:
            # 기사 전문 생성
            full_text = f"{article.get('title', '')}. {article.get('description', '')} {article.get('content', '')}"
            
            # GPT 요약
            gpt_summary = summarize_with_gpt(full_text, max_sentences, model)
            
            # 원본 기사에 GPT 요약 추가
            article_with_summary = {**article, "gpt_summary": gpt_summary}
            summarized_articles.append(article_with_summary)
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"기사 요약 실패: {error_msg}")
            
            # 429 에러 (할당량 초과) 또는 401 에러 (인증 실패) 시 조기 종료
            if "429" in error_msg or "insufficient_quota" in error_msg or "401" in error_msg:
                logger.warning("API 할당량 초과 또는 인증 실패. GPT 요약을 중단하고 원본 기사를 반환합니다.")
                # 이미 요약된 기사와 나머지 원본 기사를 모두 반환
                remaining_articles = articles[len(summarized_articles):]
                return summarized_articles + remaining_articles
            
            # 그 외 에러는 해당 기사만 건너뛰고 계속
            summarized_articles.append(article)
    
    return summarized_articles


def get_available_models() -> list[str]:
    """
    사용 가능한 GPT 모델 목록을 반환합니다.
    
    Returns:
        모델 이름 리스트
    """
    return [
        "gpt-4o-mini",      # 추천! 저렴하고 빠름 ($0.15 / 1M tokens)
        "gpt-4o",           # 더 정확하지만 비쌈 ($2.50 / 1M tokens)
        "gpt-4-turbo",      # GPT-4 터보
        "gpt-3.5-turbo"     # 가장 저렴 ($0.50 / 1M tokens)
    ]


def estimate_cost(text_length: int, model: str = "gpt-4o-mini") -> float:
    """
    요약 비용을 추정합니다 (USD).
    
    Args:
        text_length: 입력 텍스트 길이 (문자 수)
        model: 사용할 모델
    
    Returns:
        예상 비용 (달러)
    """
    # 대략적인 토큰 계산 (한글: ~1.5자/토큰, 영문: ~4자/토큰)
    estimated_tokens = text_length / 2
    
    # 모델별 비용 (per 1M tokens)
    pricing = {
        "gpt-4o-mini": 0.15,
        "gpt-4o": 2.50,
        "gpt-4-turbo": 10.00,
        "gpt-3.5-turbo": 0.50
    }
    
    price_per_million = pricing.get(model, 0.15)
    cost = (estimated_tokens / 1_000_000) * price_per_million
    
    return cost

