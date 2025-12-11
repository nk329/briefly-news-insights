"""
워드클라우드 이미지 생성 서비스
KoNLPy로 추출한 키워드를 시각화
"""

from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')  # GUI 없이 이미지 생성
import matplotlib.pyplot as plt
import os
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def generate_wordcloud(
    keywords: dict[str, int],
    output_dir: str = "static/wordcloud",
    width: int = 600,
    height: int = 400
) -> str:
    """
    키워드 딕셔너리로부터 워드클라우드 이미지를 생성합니다.
    
    Args:
        keywords: {"단어": 빈도수} 형태의 딕셔너리
        output_dir: 이미지 저장 디렉토리
        width: 이미지 너비
        height: 이미지 높이
    
    Returns:
        생성된 이미지의 URL 경로 (예: "/static/wordcloud/wordcloud_20251212_123456.png")
    """
    if not keywords:
        logger.warning("키워드가 비어있습니다.")
        return ""
    
    try:
        # 한글 폰트 경로 설정 (OS별)
        import platform
        
        if platform.system() == 'Windows':
            # Windows
            font_path = "C:/Windows/Fonts/malgun.ttf"
            if not os.path.exists(font_path):
                font_path = "C:/Windows/Fonts/gulim.ttc"
        else:
            # Linux (Ubuntu)
            font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
            if not os.path.exists(font_path):
                font_path = "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf"
        
        # 최종 폰트 파일 확인
        if not os.path.exists(font_path):
            logger.error(f"폰트 파일을 찾을 수 없습니다: {font_path}")
            raise FileNotFoundError(f"한글 폰트를 찾을 수 없습니다: {font_path}")
        
        # 워드클라우드 생성
        wc = WordCloud(
            width=width,
            height=height,
            background_color='white',
            font_path=font_path,
            max_words=100,
            relative_scaling=0.3,
            min_font_size=10,
            colormap='viridis'
        ).generate_from_frequencies(keywords)
        
        # 출력 디렉토리 생성
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 파일명 생성 (타임스탬프 포함)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"wordcloud_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        
        # 이미지 저장
        plt.figure(figsize=(width/100, height/100), dpi=100)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(filepath, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        
        # URL 경로 반환
        url_path = f"/api/wordcloud/{filename}"
        logger.info(f"워드클라우드 생성 완료: {url_path}")
        
        return url_path
        
    except Exception as e:
        logger.error(f"워드클라우드 생성 중 에러 발생: {e}")
        raise


def cleanup_old_wordclouds(
    output_dir: str = "static/wordcloud",
    max_age_hours: int = 24
) -> int:
    """
    오래된 워드클라우드 이미지를 삭제합니다.
    
    Args:
        output_dir: 이미지 디렉토리
        max_age_hours: 보관 기간 (시간)
    
    Returns:
        삭제된 파일 개수
    """
    if not os.path.exists(output_dir):
        return 0
    
    now = datetime.now()
    deleted_count = 0
    
    try:
        for filename in os.listdir(output_dir):
            if not filename.startswith('wordcloud_') or not filename.endswith('.png'):
                continue
            
            filepath = os.path.join(output_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            age_hours = (now - file_time).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                os.remove(filepath)
                deleted_count += 1
                logger.info(f"오래된 워드클라우드 삭제: {filename}")
        
        return deleted_count
        
    except Exception as e:
        logger.error(f"워드클라우드 정리 중 에러 발생: {e}")
        return deleted_count

