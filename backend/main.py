# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rooms.routes import router as rooms_router
from games.game_1.routes import router as game_1_router
import logging
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    for route in app.routes:
        if hasattr(route, "websocket_endpoint"):
            print(f"WebSocket Path: {route.path}")
        elif hasattr(route, "methods"):
            print(f"Path: {route.path}, Methods: {route.methods}")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# prefix="/room" → 결국 /room/... 형태로 REST, WS 엔드포인트 노출
app.include_router(rooms_router, prefix="/room", tags=["Room"])
app.include_router(game_1_router, prefix="/game_1", tags=["Game 1"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request path: {request.url.path}, Method: {request.method}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
