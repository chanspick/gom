from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rooms.routes import router as rooms_router
from games.game_1.routes import router as game_1_router
import logging
from contextlib import asynccontextmanager

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("main")

# Lifespan 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    print("Registered Routes:")

    for route in app.routes:
        # WebSocket 경로인지 확인
        if hasattr(route, "websocket_endpoint"):
            print(f"WebSocket Path: {route.path}")
        # HTTP 경로인지 확인
        elif hasattr(route, "methods"):
            print(f"Path: {route.path}, Methods: {route.methods}")
    
    yield  # FastAPI 서버 실행 중

    print("Shutting down...")

# FastAPI 앱 생성
app = FastAPI(lifespan=lifespan)

# 라우터 추가 (prefix 수정)
app.include_router(rooms_router, prefix="/room", tags=["Room"])  # 수정: /rooms → /room
app.include_router(game_1_router, prefix="/game_1", tags=["Game 1"])

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요한 경우 특정 도메인으로 제한 가능
    allow_methods=["*"], 
    allow_headers=["*"],
)

# HTTP 요청 로깅 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}, Method: {request.method}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
