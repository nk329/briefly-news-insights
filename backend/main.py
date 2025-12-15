from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sys

# FastAPI 앱 생성
app = FastAPI(
    title="Briefly News Insights API",
    version="1.0.0",
)

# CORS 설정 - 모든 origin 허용 (개발 환경)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
# 성능 및 안정성 문제로 분석 라우터(analysis) 일시 비활성화
from api import news, auth, history, category  # analysis 임시 제외

app.include_router(auth.router)
app.include_router(news.router)
# app.include_router(analysis.router)  # Java/SIGBUS 문제로 비활성화
app.include_router(history.router)
app.include_router(category.router)

# 정적 파일 마운트 (API 라우터 다음에)
static_dir = Path("static/wordcloud")
static_dir.mkdir(parents=True, exist_ok=True)

# 워드클라우드 이미지 서빙을 위한 별도 라우트 추가
@app.get("/api/wordcloud/{filename}")
async def serve_wordcloud(filename: str):
    from fastapi.responses import FileResponse
    file_path = static_dir / filename
    if file_path.exists():
        return FileResponse(file_path)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Image not found")

# 기타 정적 파일
app.mount("/static", StaticFiles(directory="static"), name="static")


# Startup 이벤트: 데이터베이스 초기화
@app.on_event("startup")
async def startup_event():
    try:
        from database import init_db
        init_db()
        print("[OK] Database initialized", file=sys.stderr)
    except Exception as e:
        print(f"[WARNING] Database init failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()


@app.get("/")
async def root():
    return {
        "message": "Briefly News Insights API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
