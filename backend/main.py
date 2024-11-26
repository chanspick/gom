from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rooms.routes import router as rooms_router
from games.game_1.routes import router as game_1_router
# main.py
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,  # 로그 레벨 설정
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("main")  # 모듈 이름 지정

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms_router, prefix="/rooms", tags=["Rooms"])
app.include_router(game_1_router, prefix="/game_1", tags=["Game 1"])
