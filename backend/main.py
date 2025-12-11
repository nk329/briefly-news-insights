from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import news, analysis

app = FastAPI(title="Briefly News Insights API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(news.router)
app.include_router(analysis.router)

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