from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import logging
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

# WebSocket 연결 관리
connections: Dict[str, List[WebSocket]] = {}


router = APIRouter()
logger = logging.getLogger("rooms")
# 전역 저장소 (데모용, 데이터베이스 대체)
rooms: Dict[str, Dict] = {}

# 요청 데이터 모델
class CreateRoomRequest(BaseModel):
    room_id: str

class JoinRoomRequest(BaseModel):
    player_name: str



@router.websocket("/{room_id}/ws")
async def room_websocket(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in connections:
        connections[room_id] = []
    connections[room_id].append(websocket)

    logger.info(f"WebSocket connection established for room {room_id}")

    try:
        while True:
            # 클라이언트 메시지를 수신할 수 있음 (필요 시)
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections[room_id].remove(websocket)
        logger.info(f"WebSocket connection closed for room {room_id}")


async def broadcast_room_state(room_id: str):
    if room_id in connections:
        room_state = rooms[room_id]
        logger.info(f"Broadcasting room state for room {room_id}: {room_state}")
        for websocket in connections[room_id]:
            try:
                await websocket.send_json(room_state)
            except Exception as e:
                logger.error(f"Failed to send room state to WebSocket: {e}")


@router.get("/")
def get_rooms():
    """
    모든 게임 방 목록 반환
    """
    logger.info(f"Returning all rooms: {rooms}")
    return list(rooms.values())


@router.post("/")
def create_room(request: CreateRoomRequest):
    """
    새로운 방 생성
    """
    if request.room_id in rooms:
        raise HTTPException(status_code=400, detail="Room already exists")
    rooms[request.room_id] = {
        "room_id": request.room_id,
        "players": [],
        "game_started": False,
        "game_state": None
    }
    return {"message": "Room created", "room": rooms[request.room_id]}

@router.post("/{room_id}/join")
async def join_room(room_id: str, request: JoinRoomRequest):
    logger.info(f"JoinRoom API called for room_id={room_id}, player_name={request.player_name}")
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")

    room = rooms[room_id]

    # 요청 데이터 확인
    logger.info(f"Join request: room_id={room_id}, player_name={request.player_name}")

    # 방 인원 초과 확인
    if len(room["players"]) >= 2:
        logger.warning(f"Room {room_id} is full. Current players: {room['players']}")
        raise HTTPException(status_code=400, detail="Room is full")

    # 플레이어 중복 확인
    if request.player_name in room["players"]:
        logger.warning(f"Player {request.player_name} is already in room {room_id}")
        return {"message": f"Player {request.player_name} is already in the room", "room": room}

    # 플레이어 추가
    room["players"].append(request.player_name)
    logger.info(f"Player {request.player_name} added to room {room_id}. Current players: {room['players']}")

    # 게임 상태 업데이트
    if len(room["players"]) == 2:
        try:
            room["game_started"] = True
            room["game_state"] = initialize_game(room["players"])
            room["status"] = "playing"
            logger.info(f"Game started in room {room_id} with players: {room['players']}")
        except Exception as e:
            logger.error(f"Failed to initialize game in room {room_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Game initialization failed: {e}")
    else:
        room["status"] = "waiting"

    # WebSocket 상태 브로드캐스트
    await broadcast_room_state(room_id)

    return {"message": f"Player {request.player_name} joined room {room_id}", "room": room}



@router.get("/{room_id}/state")
def get_room_state(room_id: str):
    """
    특정 방의 상태 반환
    """
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    return rooms[room_id]

@router.delete("/{room_id}")
def delete_room(room_id: str):
    """
    게임 방 삭제
    """
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    del rooms[room_id]
    return {"message": f"Room {room_id} deleted"}

def initialize_game(players: List[str]):
    """
    게임 상태 초기화
    """
    logger.info(f"Initializing game with players: {players}")
    try:
        game_state = {
            "players": {player: {"chips": 30, "card": None} for player in players},
            "current_turn": players[0],
            "pot": 0,
            "round_completed": False,
            "game_round": 1,
            "winner": None,
        }
        logger.info(f"Game initialized successfully: {game_state}")
        return game_state
    except Exception as e:
        logger.error(f"Error initializing game: {e}")
        raise
