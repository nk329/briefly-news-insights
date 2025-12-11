# 📰 Briefly News Insights - 완전 가이드

뉴스 요약 및 키워드 분석 대시보드 프로젝트

**저장소**: https://github.com/nk329/briefly-news-insights  
**구조**: 모노레포 (백엔드 + 프론트엔드)

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [기술 스택](#기술-스택)
3. [폴더 구조](#폴더-구조)
4. [빠른 시작](#빠른-시작)
5. [개발 워크플로우](#개발-워크플로우)
6. [API 설계](#api-설계)
7. [Git 관리](#git-관리)
8. [AWS 배포](#aws-배포)
9. [CI/CD 자동화](#cicd-자동화)
10. [트러블슈팅](#트러블슈팅)

---

## 🎯 프로젝트 개요

### 현재 진행 상황
- ✅ **Phase 1**: 뉴스 검색 기능 완료
- ✅ **Phase 2**: TF-IDF 요약 기능 완료
- ✅ **Phase 3**: 키워드 분석 완료
- ✅ **Phase 4**: 워드클라우드 완료
- ✅ **Phase 5**: AWS 배포 완료 (EC2: 43.201.109.211)

### 주요 기능
- 🔍 **뉴스 검색**: 키워드 기반 최신 뉴스 수집 ✅
- 📝 **자동 요약**: TF-IDF 기반 핵심 문장 추출 ✅
- 📊 **키워드 분석**: KoNLPy 형태소 분석 및 TOP 6 랭킹 표시 ✅
- ☁️ **워드클라우드**: 한글 지원 워드클라우드 이미지 생성 ✅

### 시스템 아키텍처
```
[사용자]
   ↓
[React 프론트엔드] ← HTTP → [FastAPI 백엔드]
   ↓                            ↓
[대시보드 UI]              [NewsAPI]
   - 검색                      ↓
   - 요약 표시           [텍스트 분석]
   - 키워드 차트         [워드클라우드]
   - 워드클라우드              ↓
                         [정적 파일]
```

---

## 🛠️ 기술 스택

### 백엔드 (backend/)
```
언어: Python 3.11+
프레임워크: FastAPI
뉴스 데이터: NewsAPI
텍스트 분석: KoNLPy (Okt, Mecab)
요약: TF-IDF (scikit-learn)
워드클라우드: wordcloud
서버: uvicorn, gunicorn
```

### 프론트엔드 (frontend/)
```
언어: TypeScript
프레임워크: React 18
HTTP: Axios
차트: Recharts
UI: Material-UI / Ant Design
빌드: Vite / CRA
```

### 인프라
```
서버: AWS EC2 (Ubuntu)
웹서버: Nginx (리버스 프록시)
CI/CD: GitHub Actions
도메인/SSL: Route 53 + Certificate Manager (선택)
```

---

## 📁 폴더 구조

```
briefly-news-insights/
├── .git/
├── .github/
│   └── workflows/
│       ├── backend-deploy.yml      # 백엔드 자동 배포
│       └── frontend-deploy.yml     # 프론트엔드 자동 배포
├── .gitignore                      # 통합 gitignore
├── .cursorrules                    # Cursor AI 설정
├── README.md
│
├── backend/                        # 백엔드 프로젝트
│   ├── main.py                     # FastAPI 진입점
│   ├── requirements.txt
│   ├── requirements-dev.txt        # 개발 도구
│   ├── .env.example
│   ├── .flake8                     # 린트 설정
│   │
│   ├── api/                        # API 라우터
│   │   ├── __init__.py
│   │   ├── news.py                 # 뉴스 검색
│   │   └── analysis.py             # 분석
│   │
│   ├── services/                   # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── news_service.py
│   │   ├── summarizer.py
│   │   ├── keyword_analyzer.py
│   │   └── wordcloud_generator.py
│   │
│   ├── models/                     # Pydantic 모델
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── utils/                      # 유틸리티
│   │   ├── __init__.py
│   │   └── helpers.py
│   │
│   ├── static/                     # 정적 파일
│   │   └── wordcloud/
│   │
│   └── scripts/
│       └── deploy.sh               # 배포 스크립트
│
└── frontend/                       # 프론트엔드 프로젝트
    ├── package.json
    ├── tsconfig.json
    ├── .eslintrc.json
    │
    ├── public/
    │   └── index.html
    │
    ├── src/
    │   ├── assets/                 # 이미지, 폰트
    │   │
    │   ├── components/             # 재사용 컴포넌트
    │   │   ├── SearchBar.tsx
    │   │   ├── NewsList.tsx
    │   │   ├── NewsCard.tsx
    │   │   ├── KeywordChart.tsx
    │   │   └── WordCloud.tsx
    │   │
    │   ├── screens/                # 페이지
    │   │   └── Dashboard.tsx
    │   │
    │   ├── services/               # API 호출
    │   │   └── api.service.ts
    │   │
    │   ├── types/                  # TypeScript 타입
    │   │   └── news.types.ts
    │   │
    │   ├── contexts/               # Context API
    │   │   └── NewsContext.tsx
    │   │
    │   ├── utils/                  # 헬퍼 함수
    │   │   └── helpers.ts
    │   │
    │   ├── styles/
    │   │   └── global.css
    │   │
    │   ├── App.tsx
    │   └── index.tsx
    │
    └── scripts/
        └── deploy.sh
```

---

## 🚀 빠른 시작

### 1. 저장소 클론

```powershell
cd D:\toy
git clone https://github.com/nk329/briefly-news-insights.git
cd briefly-news-insights
```

### 2. .gitignore 추가

```powershell
# toy 폴더에 있는 monorepo-.gitignore 복사
copy ..\monorepo-.gitignore .gitignore
```

### 3. README 작성

```powershell
code README.md
```

**기본 템플릿**:
```markdown
# 📰 Briefly News Insights

뉴스 요약 및 키워드 분석 대시보드

## 🎯 주요 기능
- 뉴스 검색/요약
- 키워드 분석
- 워드클라우드

## 🛠️ 기술 스택
- Backend: Python FastAPI
- Frontend: React TypeScript

## 🚀 실행 방법
자세한 내용은 PROJECT_GUIDE.md 참고
```

### 4. 백엔드 프로젝트 생성

```powershell
# 백엔드 폴더 생성
mkdir backend
cd backend

# Python 가상환경
python -m venv venv
.\venv\Scripts\activate

# FastAPI 설치
pip install fastapi uvicorn python-dotenv requests
pip freeze > requirements.txt

# 개발 도구 설치
pip install flake8 black pytest
pip freeze > requirements-dev.txt

# 기본 구조 생성
mkdir api, services, models, utils, static\wordcloud, scripts
New-Item -ItemType File -Name "main.py"
New-Item -ItemType File -Name ".env.example"
```

**main.py 기본 코드**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Briefly News Insights API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Briefly News Insights API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**테스트**:
```powershell
uvicorn main:app --reload
# http://localhost:8000 접속 확인
```

### 5. 프론트엔드 프로젝트 생성

```powershell
# 루트로 이동
cd D:\toy\briefly-news-insights

# React 프로젝트
npx create-react-app frontend --template typescript

cd frontend

# 패키지 설치
npm install axios react-router-dom recharts

# 테스트
npm start
# http://localhost:3000 확인
```

### 6. 첫 커밋

```powershell
cd D:\toy\briefly-news-insights
git add .
git commit -m "feat: 프로젝트 초기 설정 (backend + frontend)"
git push origin main
```

---

## 🔄 개발 워크플로우

### Phase 1: MVP (뉴스 검색)

#### 백엔드
```powershell
cd backend
.\venv\Scripts\activate

# NewsAPI 패키지 설치
pip install newsapi-python
pip freeze > requirements.txt

# .env 파일 생성
echo NEWS_API_KEY=your_api_key > .env
```

**api/news.py** 작성:
```python
from fastapi import APIRouter, Query
from newsapi import NewsApiClient
import os

router = APIRouter(prefix="/api/news", tags=["news"])
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

@router.get("/search")
async def search_news(
    keyword: str = Query(..., description="검색 키워드"),
    from_date: str = Query(None, description="시작일 (YYYY-MM-DD)"),
    to_date: str = Query(None, description="종료일 (YYYY-MM-DD)"),
    page_size: int = Query(10, ge=1, le=100)
):
    """뉴스 검색 API"""
    try:
        response = newsapi.get_everything(
            q=keyword,
            from_param=from_date,
            to=to_date,
            language='ko',
            sort_by='publishedAt',
            page_size=page_size
        )
        
        return {
            "status": "success",
            "data": {
                "total": response['totalResults'],
                "articles": response['articles']
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

**main.py에 라우터 추가**:
```python
from api import news

app.include_router(news.router)
```

#### 프론트엔드

**src/services/api.service.ts**:
```typescript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const searchNews = async (keyword: string, fromDate?: string, toDate?: string) => {
  const response = await axios.get(`${API_BASE_URL}/api/news/search`, {
    params: { keyword, from_date: fromDate, to_date: toDate }
  });
  return response.data;
};
```

**src/components/SearchBar.tsx**:
```typescript
import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (keyword: string, from?: string, to?: string) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [keyword, setKeyword] = useState('');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(keyword, fromDate, toDate);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="검색 키워드"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        required
      />
      <input type="date" value={fromDate} onChange={(e) => setFromDate(e.target.value)} />
      <input type="date" value={toDate} onChange={(e) => setToDate(e.target.value)} />
      <button type="submit">검색</button>
    </form>
  );
};
```

---

### Phase 2: 요약 기능 ✅ 완료

**백엔드 구현**:
```powershell
cd backend
pip install scikit-learn nltk
pip freeze > requirements.txt
```

**services/summarizer.py**:
- TF-IDF 기반 추출적 요약
- 문장 분리 및 중요도 계산
- 상위 N개 문장 추출
- 원본 순서 유지

**api/news.py 수정**:
- `summarize` 파라미터 추가 (기본 True)
- 검색 결과에 자동 요약 통합
- `summary` 필드 추가

**프론트엔드 구현**:
- NewsList.tsx 수정
- "✨ AI 요약" 뱃지 스타일
- 요약문 하이라이트 박스

**결과**: 
- 뉴스 검색 시 자동으로 3문장 요약 제공
- 파란색 박스로 요약 강조 표시

---

### Phase 3: 키워드 분석 ✅ 완료

**백엔드 구현**:
```powershell
cd backend
pip install konlpy
pip freeze > requirements.txt
```

**services/keyword_analyzer.py**:
```python
from konlpy.tag import Okt
from collections import Counter
import logging

logger = logging.getLogger(__name__)
okt = Okt()

def analyze_keywords(texts: list[str], top_n: int = 20) -> dict:
    """
    주어진 텍스트 목록에서 키워드를 분석하고 빈도수를 반환합니다.
    명사만 추출하며, 한 글자 단어 및 불용어는 제외합니다.
    """
    if not texts:
        return {"keywords": [], "total_words": 0}

    combined_text = ' '.join(texts)
    
    # 명사 추출
    try:
        nouns = okt.nouns(combined_text)
    except Exception as e:
        logger.error(f"KoNLPy 명사 추출 중 에러 발생: {e}")
        return {"keywords": [], "total_words": 0}

    # 불용어 정의 (확장 가능)
    stopwords = [
        '것', '수', '때', '년', '월', '일', '이', '그', '저', '등', '및', 
        '더', '말', '안', '점', '위', '분', '개', '내', '전', '데', '중', '곳'
    ]
    
    # 한 글자 단어 및 불용어 제거
    filtered_nouns = [
        word for word in nouns 
        if len(word) > 1 and word not in stopwords
    ]
    
    # 빈도 계산
    counter = Counter(filtered_nouns)
    
    keywords_data = [
        {"word": word, "count": count}
        for word, count in counter.most_common(top_n)
    ]
    
    logger.info(f"키워드 분석 완료: {len(keywords_data)}개 키워드, 총 {len(filtered_nouns)} 단어")
    return {"keywords": keywords_data, "total_words": len(filtered_nouns)}
```

**api/analysis.py**:
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.keyword_analyzer import analyze_keywords

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

class ArticleContent(BaseModel):
    title: str
    description: str | None = None
    content: str | None = None

class ArticleKeywordAnalysisRequest(BaseModel):
    articles: List[ArticleContent]
    top_n: int = 20

@router.post("/articles/keywords")
async def get_keywords_from_articles(request: ArticleKeywordAnalysisRequest):
    """
    주어진 기사 목록에서 키워드를 추출하고 빈도수를 반환합니다.
    기사의 title, description, content 필드를 모두 사용하여 분석합니다.
    """
    try:
        all_texts = []
        for article in request.articles:
            all_texts.append(article.title or "")
            all_texts.append(article.description or "")
            all_texts.append(article.content or "")
        
        # 빈 문자열 제거
        all_texts = [text for text in all_texts if text.strip()]

        result = analyze_keywords(all_texts, request.top_n)
        result["analyzed_articles"] = len(request.articles)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"기사 키워드 분석 실패: {str(e)}")
```

**main.py에 라우터 추가**:
```python
from api import news, analysis

app.include_router(news.router)
app.include_router(analysis.router)
```

**프론트엔드 구현**:

**src/services/api.service.ts**:
```typescript
export const analyzeArticlesKeywords = async (
  articles: NewsArticle[],
  topN: number = 6
): Promise<KeywordAnalysisResponse> => {
  try {
    const response = await axios.post<KeywordAnalysisResponse>(
      `${API_BASE_URL}/api/analysis/articles/keywords`,
      { articles, top_n: topN }
    );
    return response.data;
  } catch (error) {
    console.error('키워드 분석 실패:', error);
    throw error;
  }
};
```

**src/components/KeywordChart.tsx**:
- TOP 6 키워드 랭킹 표시
- 검색어 기반 동적 제목: `"호날두" 관련 인기 키워드`
- 날짜 기준 표시
- Sticky 레이아웃 (스크롤 시 고정)

**src/screens/Dashboard.tsx**:
- 좌우 레이아웃 구현 (Flexbox)
- 키워드 차트 (25%) + 뉴스 리스트 (75%)
- 뉴스 검색 시 자동으로 키워드 분석 실행

**결과**: 
- 뉴스 검색 시 자동으로 TOP 6 키워드 추출
- 왼쪽에 키워드 랭킹, 오른쪽에 뉴스 목록
- 깔끔한 리스트 UI

---

### Phase 4: 워드클라우드 ✅ 완료

**백엔드 구현**:
```powershell
cd backend
pip install wordcloud matplotlib Pillow
pip freeze > requirements.txt
```

**services/wordcloud_generator.py**:
```python
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')  # GUI 없이 이미지 생성
import matplotlib.pyplot as plt
import os
from datetime import datetime
from pathlib import Path

def generate_wordcloud(
    keywords: dict[str, int],
    output_dir: str = "static/wordcloud",
    width: int = 600,
    height: int = 400
) -> str:
    """
    키워드 딕셔너리로부터 워드클라우드 이미지를 생성합니다.
    
    - 한글 폰트 지원 (맑은 고딕)
    - 타임스탬프 기반 파일명
    - 정적 파일 URL 반환
    """
    # 한글 폰트 설정
    font_path = "C:/Windows/Fonts/malgun.ttf"
    
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
    
    return f"/static/wordcloud/{filename}"

def cleanup_old_wordclouds(
    output_dir: str = "static/wordcloud",
    max_age_hours: int = 24
) -> int:
    """오래된 워드클라우드 이미지를 삭제합니다."""
    # 24시간 이상 된 이미지 자동 정리
    # ...구현...
```

**api/analysis.py에 엔드포인트 추가**:
```python
@router.post("/wordcloud")
async def generate_wordcloud_api(request: WordCloudRequest):
    """워드클라우드 이미지 생성"""
    # 오래된 이미지 정리
    cleanup_old_wordclouds(max_age_hours=24)
    
    # 워드클라우드 생성
    image_url = generate_wordcloud(
        keywords=request.keywords,
        width=request.width,
        height=request.height
    )
    
    return {"status": "success", "data": {"imageUrl": image_url}}

@router.post("/articles/complete")
async def complete_analysis_api(request: ArticlesKeywordRequest):
    """통합 분석 (키워드 + 워드클라우드)"""
    # 1. 키워드 분석
    result = analyze_articles_keywords(request.articles, request.top_n)
    
    # 2. 워드클라우드 생성
    keywords_dict = {item["word"]: item["count"] for item in result["keywords"]}
    cleanup_old_wordclouds(max_age_hours=24)
    image_url = generate_wordcloud(keywords=keywords_dict)
    
    return {
        "status": "success",
        "data": {**result, "wordcloudUrl": image_url}
    }
```

**main.py에 정적 파일 서빙 설정**:
```python
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# 정적 파일 디렉토리 생성
static_dir = Path("static/wordcloud")
static_dir.mkdir(parents=True, exist_ok=True)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")
```

**프론트엔드 구현**:

**src/components/WordCloud.tsx**:
```typescript
interface WordCloudProps {
  imageUrl: string;
  loading?: boolean;
  searchKeyword?: string;
}

export const WordCloud: React.FC<WordCloudProps> = ({
  imageUrl,
  loading,
  searchKeyword,
}) => {
  if (loading) {
    return <div>워드클라우드 생성 중...</div>;
  }

  if (!imageUrl) return null;

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  const fullImageUrl = `${API_BASE_URL}${imageUrl}`;

  return (
    <div style={styles.container}>
      <h3>{searchKeyword ? `"${searchKeyword}" 워드클라우드` : '워드클라우드'}</h3>
      <img src={fullImageUrl} alt="워드클라우드" style={styles.image} />
    </div>
  );
};
```

**src/services/api.service.ts**:
```typescript
export const completeAnalysis = async (
  articles: any[],
  topN: number = 20
): Promise<any> => {
  const response = await axios.post(
    `${API_BASE_URL}/api/analysis/articles/complete`,
    { articles, top_n: topN }
  );
  return response.data;
};
```

**src/screens/Dashboard.tsx**:
```typescript
// 통합 분석 호출
const analysisResponse = await completeAnalysis(fetchedArticles, 20);

// 키워드 상위 6개 표시
setKeywords(analysisResponse.data.keywords?.slice(0, 6) || []);

// 워드클라우드 URL 설정
setWordcloudUrl(analysisResponse.data.wordcloudUrl || '');

// 레이아웃: 좌(키워드) + 우(워드클라우드 + 뉴스)
<div style={styles.contentLayout}>
  <div style={styles.keywordSection}>
    <KeywordChart keywords={keywords} />
  </div>
  <div style={styles.newsSection}>
    <WordCloud imageUrl={wordcloudUrl} />
    <NewsList articles={articles} />
  </div>
</div>
```

**결과**:
- 뉴스 검색 시 자동으로 워드클라우드 생성
- 한글 키워드 정상 표시
- 600x400px 크기 (max-height: 400px)
- 24시간 후 자동 정리
- 우측 상단에 워드클라우드 배치

---

## 📡 API 설계

### 1. 뉴스 검색
```http
GET /api/news/search?keyword=AI&from=2025-01-01&to=2025-12-31&page_size=10
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total": 42,
    "articles": [
      {
        "title": "뉴스 제목",
        "source": {"name": "언론사"},
        "url": "https://...",
        "publishedAt": "2025-12-11T10:00:00Z",
        "content": "기사 본문..."
      }
    ]
  }
}
```

### 2. 키워드 분석
```http
POST /api/analysis/keywords
Content-Type: application/json

{
  "texts": ["기사1", "기사2"],
  "top_n": 20
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "keywords": [
      {"word": "인공지능", "count": 45},
      {"word": "기술", "count": 32}
    ]
  }
}
```

### 3. 워드클라우드
```http
POST /api/analysis/wordcloud
Content-Type: application/json

{
  "keywords": {"인공지능": 45, "기술": 32}
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "imageUrl": "/static/wordcloud/wordcloud_20251211_103000.png"
  }
}
```

### 4. 통합 분석 (권장)
```http
POST /api/analysis/complete
Content-Type: application/json

{
  "keyword": "AI",
  "from": "2025-12-01",
  "to": "2025-12-11"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "articles": [...],
    "keywords": [...],
    "wordcloudUrl": "...",
    "statistics": {
      "totalArticles": 42
    }
  }
}
```

---

## 🔧 Git 관리

### 커밋 메시지 규칙

```
<type>(scope): <subject>

type:
- feat: 새 기능
- fix: 버그 수정
- docs: 문서
- style: 포맷팅
- refactor: 리팩토링
- test: 테스트
- chore: 설정

scope: backend, frontend, docs

예시:
feat(backend): 뉴스 검색 API 추가
fix(frontend): 검색 버튼 클릭 오류 수정
docs: README 업데이트
```

### 일상적인 작업

```powershell
# 1. 최신 코드 받기
git pull origin main

# 2. 작업

# 3. 커밋
git status
git add .
git commit -m "feat(backend): 키워드 분석 기능 추가"
git push origin main
```

### 환경 변수 관리

**.env 파일 (절대 커밋 금지!)**:
```env
NEWS_API_KEY=your_actual_key
PORT=8000
DEBUG=True
```

**.env.example (Git에 커밋)**:
```env
NEWS_API_KEY=your_news_api_key
PORT=8000
DEBUG=False
```

---

## ☁️ AWS 배포

### 1. EC2 인스턴스 생성 ✅

**인스턴스 정보**:
- OS: Ubuntu 24.04 LTS
- 인스턴스 유형: t2.micro (1GB RAM)
- 퍼블릭 IP: 43.201.109.211
- 키 페어: briefly-key.pem

**보안 그룹**:
```
인바운드 규칙:
- SSH (22): 내 IP
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0
```

**중요**: t2.micro는 1GB RAM이므로 Swap 파일 필수!

### 2. 서버 초기 설정 ✅

```bash
# SSH 접속
ssh -i "briefly-key.pem" ubuntu@43.201.109.211

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
sudo apt install -y python3-pip python3-venv nodejs npm nginx git

# Java 설치 (KoNLPy 필수)
sudo apt install -y openjdk-11-jdk

# 한글 폰트 설치 (워드클라우드 필수)
sudo apt install -y fonts-nanum

# JAVA_HOME 설정
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc

# Swap 파일 생성 (t2.micro는 1GB RAM이므로 필수!)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 확인
free -h  # Swap이 2G로 표시되어야 함
java --version  # OpenJDK 11 확인
```

### 3. 백엔드 배포

```bash
# 저장소 클론
git clone https://github.com/nk329/briefly-news-insights.git
cd briefly-news-insights/backend

# Python 환경
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 환경 변수
nano .env
# NEWS_API_KEY=... 입력

# Gunicorn 설치
pip install gunicorn uvicorn[standard]

# Systemd 서비스
sudo nano /etc/systemd/system/news-api.service
```

**briefly-api.service**:
```ini
[Unit]
Description=Briefly News Insights API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/briefly-news-insights/backend
Environment="PATH=/home/ubuntu/briefly-news-insights/backend/venv/bin"
Environment="JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64"
ExecStart=/home/ubuntu/briefly-news-insights/backend/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b 127.0.0.1:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 서비스 파일 생성
sudo nano /etc/systemd/system/briefly-api.service

# 서비스 시작
sudo systemctl daemon-reload
sudo systemctl start briefly-api
sudo systemctl enable briefly-api
sudo systemctl status briefly-api

# 로그 확인
sudo journalctl -u briefly-api -f
```

### 4. 프론트엔드 배포

```bash
cd ~/briefly-news-insights/frontend

# 환경 변수
nano .env
# REACT_APP_API_URL=http://your-ec2-ip/api

# 빌드
npm install
npm run build
```

### 5. Nginx 설정 ✅

```bash
sudo nano /etc/nginx/sites-available/briefly-news
```

```nginx
server {
    listen 80;
    server_name 43.201.109.211;

    # 프론트엔드
    root /home/ubuntu/briefly-news-insights/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 워드클라우드 이미지 (이 블록이 /api/ 보다 먼저 와야 함!)
    location /api/wordcloud/ {
        alias /home/ubuntu/briefly-news-insights/backend/static/wordcloud/;
        expires 1h;
        add_header Cache-Control "public, immutable";
    }

    # 백엔드 API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
    }
}
```

```bash
# Nginx 활성화
sudo ln -s /etc/nginx/sites-available/briefly-news /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 권한 설정 (중요!)
chmod -R 755 ~/briefly-news-insights
chmod 755 /home/ubuntu
```

### 6. SSL 인증서 (선택)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 7. EC2 인스턴스 관리

**인스턴스 중지 (비용 절약)**:
```
AWS Console → EC2 → 인스턴스 선택 → 인스턴스 상태 → 중지
```
- 중지 시: EBS 스토리지 비용만 발생 (매우 저렴)
- 퍼블릭 IP는 변경될 수 있음 (Elastic IP 사용 권장)

**인스턴스 시작 (재개)**:
```
AWS Console → EC2 → 인스턴스 선택 → 인스턴스 상태 → 시작
```
- 새 퍼블릭 IP 확인 (변경되었을 수 있음)
- SSH 재접속: `ssh -i briefly-key.pem ubuntu@새로운_IP`
- 서비스는 자동으로 시작됨 (systemd enable 설정 완료)

**인스턴스 종료 (삭제)**:
```
AWS Console → EC2 → 인스턴스 선택 → 인스턴스 상태 → 종료
```
- ⚠️ 모든 데이터 영구 삭제!
- 복구 불가능하므로 주의!

---

## 🤖 CI/CD 자동화

### GitHub Secrets 설정

**저장소 → Settings → Secrets and variables → Actions**

추가할 Secrets:
- `EC2_HOST`: EC2 공개 IP
- `EC2_USERNAME`: ubuntu
- `EC2_SSH_KEY`: .pem 파일 전체 내용
- `NEWS_API_KEY`: NewsAPI 키
- `REACT_APP_API_URL`: API URL

### 워크플로우 파일

**.github/workflows/backend-deploy.yml**:
```yaml
name: Backend Deploy

on:
  push:
    branches: [main]
    paths: ['backend/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/briefly-news-insights/backend
            git pull origin main
            source venv/bin/activate
            pip install -r requirements.txt
            sudo systemctl restart news-api
```

**.github/workflows/frontend-deploy.yml**:
```yaml
name: Frontend Deploy

on:
  push:
    branches: [main]
    paths: ['frontend/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/briefly-news-insights/frontend
            git pull origin main
            npm install
            npm run build
            sudo systemctl reload nginx
```

### EC2 sudo 권한 설정

```bash
sudo visudo
```

맨 아래 추가:
```
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl restart news-api
ubuntu ALL=(ALL) NOPASSWD: /bin/systemctl reload nginx
```

---

## 🔍 트러블슈팅

### 1. SSH 연결 실패
```
에러: Permission denied (publickey)

해결:
- GitHub Secrets의 EC2_SSH_KEY 확인
- .pem 파일 전체 내용 (BEGIN/END 포함)
- EC2 보안 그룹 SSH 포트 확인
```

### 2. API 호출 실패
```
에러: CORS policy error

해결:
백엔드 main.py에서 CORS 설정 확인
allow_origins에 프론트엔드 URL 추가
```

### 3. 한글 깨짐
```
에러: 워드클라우드 한글 깨짐

해결:
sudo apt install fonts-nanum -y
font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
```

### 4. 서비스 시작 실패
```
에러: Service failed to start

해결:
sudo journalctl -u news-api -n 50
로그 확인 후 에러 수정
```

### 5. Nginx 502 Bad Gateway
```
에러: 502 Bad Gateway

해결:
sudo systemctl status briefly-api  # 백엔드 실행 확인
sudo netstat -tlnp | grep 8000  # 포트 확인
```

### 6. 메모리 부족 (npm build)
```
에러: npm run build가 멈추거나 매우 느림

해결: Swap 파일 생성 (t2.micro는 1GB RAM이므로 필수)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 영구 설정
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 7. Nginx Permission Denied
```
에러: stat() failed (13: Permission denied)

해결: 프론트엔드 build 폴더 권한 설정
chmod -R 755 ~/briefly-news-insights
chmod 755 /home/ubuntu
```

### 8. KoNLPy Java 에러
```
에러: No JVM shared library file (libjvm.so) found

해결: Java 설치 및 JAVA_HOME 설정
sudo apt install -y openjdk-11-jdk
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc

# 또는 systemd 서비스 파일에 직접 추가
[Service]
Environment="JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64"
```

### 9. 워드클라우드 404 에러
```
에러: /api/wordcloud/wordcloud_xxx.png 404 Not Found

해결: Nginx 설정에서 /api/wordcloud/ location 추가
location /api/wordcloud/ {
    alias /home/ubuntu/briefly-news-insights/backend/static/wordcloud/;
    expires 1h;
    add_header Cache-Control "public, immutable";
}

# 이 블록은 /api/ 블록보다 먼저 와야 함!
```

---

## 📊 개발 체크리스트

### Phase 1: MVP ✅ **완료**
- [x] 백엔드 기본 구조
- [x] 뉴스 API 연동
- [x] 프론트엔드 기본 UI
- [x] 검색 기능
- [x] 로컬 환경 테스트

### Phase 2: 요약 ✅ **완료**
- [x] TF-IDF 기반 요약 엔진
- [x] 뉴스 검색 API에 요약 통합
- [x] 요약 UI (✨ AI 요약 뱃지)
- [x] 로컬 테스트 성공

### Phase 3: 키워드 분석 ✅ **완료**
- [x] KoNLPy 설치 및 설정
- [x] 키워드 추출 서비스 (keyword_analyzer.py)
- [x] 키워드 분석 API (/api/analysis/articles/keywords)
- [x] TOP 6 키워드 랭킹 UI (KeywordChart.tsx)
- [x] 좌우 레이아웃 (키워드 1 : 뉴스 3)
- [x] 동적 제목 ("검색어" 관련 인기 키워드)
- [x] Sticky 레이아웃 (스크롤 고정)

### Phase 4: 워드클라우드 ✅ **완료**
- [x] wordcloud, matplotlib, Pillow 패키지 설치
- [x] 이미지 생성 서비스 (wordcloud_generator.py)
- [x] 워드클라우드 API (/api/analysis/wordcloud)
- [x] 통합 분석 API (/api/analysis/articles/complete)
- [x] 정적 파일 서빙 (FastAPI StaticFiles)
- [x] WordCloud 컴포넌트 작성
- [x] Dashboard에 워드클라우드 통합
- [x] 한글 폰트 지원 (맑은 고딕)
- [x] 이미지 크기 최적화 (600x400px)
- [x] 오래된 이미지 자동 정리 (24시간)

### Phase 5: 배포 ✅ **완료**
- [x] EC2 인스턴스 생성 (Ubuntu 24.04, t2.micro)
- [x] Swap 파일 생성 (2GB)
- [x] 서버 초기 설정 (Python, Node.js, Nginx, Git, Java, Fonts)
- [x] 백엔드 배포 (Gunicorn + Systemd)
- [x] 프론트엔드 배포 (npm build)
- [x] Nginx 설정 (리버스 프록시 + 워드클라우드 정적 파일)
- [x] 최종 테스트 (검색, 요약, 키워드, 워드클라우드 모두 작동)
- [ ] CI/CD 설정 (GitHub Actions) - 선택
- [ ] SSL 인증서 (선택)
- [ ] 도메인 연결 (선택)

### Phase 6: 추가 기능 (선택) 💡
- [ ] ChatGPT API 요약 (고급 요약)
- [ ] 국가 선택 + 번역 기능
- [ ] 로그인 + MySQL
- [ ] 검색 기록 저장
- [ ] 카테고리 관리

---

## 🎓 추가 리소스

### 외부 문서
- [NewsAPI](https://newsapi.org/docs)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [KoNLPy](https://konlpy.org/)

### toy 폴더 설정 파일
```
toy/
├── monorepo-.gitignore          → .gitignore로 복사
├── backend-deploy.yml           → .github/workflows/로 복사
├── frontend-deploy.yml          → .github/workflows/로 복사
├── backend-.flake8              → backend/.flake8로 복사
├── backend-requirements-dev.txt → backend/로 복사
└── frontend-package-scripts.json → 참고용
```

---

## 💡 개발 팁

1. **가상환경 항상 활성화** 확인
2. **커밋 전 로컬 테스트** 필수
3. **.env 파일 절대 커밋 금지**
4. **의미있는 커밋 메시지** 작성
5. **자주 푸시**해서 백업

---

## 📞 빠른 명령어

### 개발 서버
```powershell
# 백엔드
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload

# 프론트엔드
cd frontend
npm start
```

### Git
```powershell
git status
git add .
git commit -m "feat(backend): 기능 추가"
git push origin main
```

### 배포 (EC2)
```bash
# 백엔드
cd ~/briefly-news-insights
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart briefly-api

# 프론트엔드
cd ~/briefly-news-insights
git pull origin main
cd frontend
npm install
npm run build
sudo systemctl reload nginx

# 상태 확인
sudo systemctl status briefly-api
sudo systemctl status nginx
```

---

**이 하나의 문서로 프로젝트 전체를 관리하세요!** 🚀

필요한 내용은 목차에서 찾아보거나 Ctrl+F로 검색하세요.




