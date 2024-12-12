# rooms/routes.py

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, List
import logging
import asyncio

connections: Dict[str, List[WebSocket]] = {}
rooms: Dict[str, Dict] = {}
rooms_lock = asyncio.Lock()

router = APIRouter()
logger = logging.getLogger("room")

class CreateRoomRequest(BaseModel):
    room_id: str
    game_type: str
    player_name: str

class JoinRoomRequest(BaseModel):
    player_name: str

@router.websocket("/{room_id}/ws")  # 변경: prefix /room이 있으므로 실제 경로는 /room/{room_id}/ws
async def room_websocket(websocket: WebSocket, room_id: str):
    logger.debug(f"Attempting WebSocket connection for room {room_id}")

    await websocket.accept()
    async with rooms_lock:
        if room_id not in rooms:
            logger.debug(f"Room {room_id} does not exist. Closing WebSocket.")
            await websocket.close(code=1008, reason="Room does not exist")
            return

        if room_id not in connections:
            connections[room_id] = []
        connections[room_id].append(websocket)
    
    logger.info(f"WebSocket connection established for room {room_id}")

    try:
        while True:
            message = await websocket.receive_text()
            logger.debug(f"Received message from room {room_id}: {message}")
            # 필요 시 메시지 처리 로직 추가
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for room {room_id}")
        async with rooms_lock:
            if room_id in connections:
                connections[room_id].remove(websocket)
                if not connections[room_id]:
                    del connections[room_id]

async def broadcast_room_state(room_id: str):
    async with rooms_lock:
        if room_id not in connections:
            return
        room_state = rooms.get(room_id)
        if not room_state:
            logger.warning(f"No state found for room {room_id}")
            return

        disconnected_clients = []
        for websocket in connections[room_id]:
            try:
                await websocket.send_json(room_state)
            except Exception as e:
                logger.error(f"Failed to send state to client: {e}")
                disconnected_clients.append(websocket)

        for websocket in disconnected_clients:
            connections[room_id].remove(websocket)
        if room_id in connections and not connections[room_id]:
            del connections[room_id]

def update_room_state(room_id: str, new_state: Dict):
    rooms[room_id] = new_state
    asyncio.create_task(broadcast_room_state(room_id))

@router.post("/")
async def create_room(request: CreateRoomRequest):
    async with rooms_lock:
        if request.room_id in rooms:
            raise HTTPException(status_code=400, detail="Room already exists")

        rooms[request.room_id] = {
            "room_id": request.room_id,
            "game_type": request.game_type,
            "players": [{"player_name": request.player_name}],
            "game_started": False,
            "game_state": initialize_game([{"player_name": request.player_name}]),
            "status": "waiting",
        }

        logger.info(f"Room {request.room_id} created by {request.player_name}")

    update_room_state(request.room_id, rooms[request.room_id])
    return {"message": "Room created successfully.", "room": rooms[request.room_id]}

@router.get("/")
async def get_rooms():
    async with rooms_lock:
        room_list = [
            {
                "room_id": room["room_id"],
                "game_type": room["game_type"],
                "status": room["status"],
                "players": [player["player_name"] for player in room["players"]],
            }
            for room in rooms.values()
        ]
        logger.info(f"Returning all rooms: {room_list}")
        return room_list

@router.post("/{room_id}/join")
async def join_room(room_id: str, request: JoinRoomRequest):
    player_name = request.player_name
    async with rooms_lock:
        if room_id not in rooms:
            raise HTTPException(status_code=404, detail="Room not found")

        room = rooms[room_id]
        if len(room["players"]) >= 2:
            raise HTTPException(status_code=400, detail="Room is full")

        if player_name in [p["player_name"] for p in room["players"]]:
            return {"message": "Player already in the room", "room": room}

        room["players"].append({"player_name": player_name})
        room["status"] = "playing" if len(room["players"]) == 2 else "waiting"

        if not room["game_started"] and len(room["players"]) == 2:
            room["game_state"] = initialize_game(room["players"])
            room["game_started"] = True

    logger.info(f"Player {player_name} joined room {room_id}")
    update_room_state(room_id, room)

    return {"message": f"Player {player_name} joined room {room_id}", "room": room}

@router.get("/{room_id}")
def get_room_state(room_id: str):
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    return rooms[room_id]

@router.delete("/{room_id}")
async def delete_room(room_id: str):
    async with rooms_lock:
        if room_id not in rooms:
            raise HTTPException(status_code=404, detail="Room not found")

        await broadcast_room_deleted(room_id)
        del rooms[room_id]
        logger.info(f"Room {room_id} deleted")

    return {"message": f"Room {room_id} deleted"}

async def broadcast_room_deleted(room_id: str):
    async with rooms_lock:
        if room_id in connections:
            for websocket in connections[room_id]:
                try:
                    await websocket.send_json({"type": "room_deleted", "room_id": room_id})
                except Exception as e:
                    logger.error(f"Failed to notify client about room deletion: {e}")
            del connections[room_id]

def initialize_game(players: List[Dict]) -> Dict:
    return {
        "players": {player["player_name"]: {"chips": 30, "card": None} for player in players},
        "current_turn": players[0]["player_name"],
        "pot": 0,
        "round_completed": False,
        "game_round": 1,
        "winner": None,
    }
