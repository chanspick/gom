from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, List
import logging
import asyncio

# WebSocket 연결 관리
connections: Dict[str, List[WebSocket]] = {}
rooms: Dict[str, Dict] = {}
rooms_lock = asyncio.Lock()

# FastAPI Router
router = APIRouter()
logger = logging.getLogger("rooms")

# 데이터 모델
class CreateRoomRequest(BaseModel):
    room_id: str
    game_type: str
    player_name: str  # 방 생성자 이름

class JoinRoomRequest(BaseModel):
    player_name: str

# WebSocket 연결 관리
@router.websocket("/{room_id}/ws")
async def room_websocket(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in connections:
        connections[room_id] = []
    connections[room_id].append(websocket)
    logger.info(f"WebSocket connection established for room {room_id}")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections[room_id].remove(websocket)
        if not connections[room_id]:
            del connections[room_id]
        logger.info(f"WebSocket connection closed for room {room_id}")

async def broadcast_room_state(room_id: str):
    async with rooms_lock:
        if room_id in connections:
            room_state = rooms.get(room_id)
            if room_state:
                logger.info(f"Broadcasting state for room {room_id}: {room_state}")
                for websocket in connections[room_id]:
                    try:
                        await websocket.send_json(room_state)
                    except Exception as e:
                        logger.error(f"Failed to send room state: {e}")


# 방 생성
@router.post("/")
async def create_room(request: CreateRoomRequest):
    """
    새로운 방 생성과 동시에 플레이어 추가
    """
    async with rooms_lock:
        if request.room_id in rooms:
            raise HTTPException(status_code=400, detail="Room already exists")
        
        # 방 생성 시 첫 번째 플레이어를 바로 추가
        rooms[request.room_id] = {
            "room_id": request.room_id,
            "game_type": request.game_type,
            "players": [{"player_name": request.player_name}],  # 딕셔너리 형태로 플레이어 추가
            "game_started": False,
            "game_state": None,
            "status": "waiting",
        }
        
        logger.info(f"Room {request.room_id} created with game type {request.game_type} by player {request.player_name}")
    
    return {"message": "Room created successfully.", "room": rooms[request.room_id]}


# 방 목록 조회
@router.get("/")
async def get_rooms():
    """
    모든 방 목록 반환
    """
    async with rooms_lock:
        room_list = [{"room_id": room["room_id"], "game_type": room["game_type"], "status": room["status"], "players": len(room["players"])} for room in rooms.values()]
        logger.info(f"Returning all rooms: {room_list}")
        return room_list

@router.post("/{room_id}/join")
async def join_room(room_id: str, request: JoinRoomRequest):
    """
    특정 방에 플레이어 추가
    """
    player_name = request.player_name
    logger.info(f"Player {player_name} attempting to join room {room_id}")
    
    async with rooms_lock:
        # 방 유무 확인
        if room_id not in rooms:
            raise HTTPException(status_code=404, detail="Room not found")
        
        room = rooms[room_id]
        
        # 방의 상태 확인
        if len(room["players"]) >= 2:
            raise HTTPException(status_code=400, detail="Room is full")
        
        # 이미 플레이어가 있는지 확인
        if player_name in [p["player_name"] for p in room["players"] if isinstance(p, dict)]:
            return {"message": "Player already in the room", "room": room}

        # 플레이어 추가 (딕셔너리 형태로 추가)
        room["players"].append({"player_name": player_name})
        
        # 게임 시작 여부 갱신
        if len(room["players"]) == 2:
            room["game_started"] = True
            room["game_state"] = initialize_game(room["players"])
            room["status"] = "playing"
            logger.info(f"Game started in room {room_id}")
        else:
            room["status"] = "waiting"
        
        await broadcast_room_state(room_id)
    
    return {"message": f"Player {player_name} joined room {room_id}", "room": room}


# 방 상태 조회
@router.get("/{room_id}")
def get_room_state(room_id: str):
    """
    특정 방의 상태 반환
    """
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    return rooms[room_id]

# 방 삭제
@router.delete("/{room_id}")
async def delete_room(room_id: str):
    """
    특정 방 삭제
    """
    async with rooms_lock:
        if room_id not in rooms:
            raise HTTPException(status_code=404, detail="Room not found")
        del rooms[room_id]
        logger.info(f"Room {room_id} deleted")
        return {"message": f"Room {room_id} deleted"}

# 게임 초기화
def initialize_game(players: List[Dict]) -> Dict:
    """
    게임 상태 초기화
    """
    try:
        return {
            "players": {player["player_name"]: {"chips": 30, "card": None} for player in players},
            "current_turn": players[0]["player_name"],
            "pot": 0,
            "round_completed": False,
            "game_round": 1,
            "winner": None,
        }
    except Exception as e:
        logger.error(f"Error initializing game: {e}")
        raise
