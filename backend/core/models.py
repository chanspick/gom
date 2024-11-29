from typing import List, Optional
from pydantic import BaseModel

class Player(BaseModel):
    player_name: str
    chips: int

class GameState(BaseModel):
    current_turn: int
    pot: int
    round_completed: bool

class Room(BaseModel):
    room_id: str
    players: List[Player]  # 플레이어들의 리스트
    game_started: bool
    game_type: Optional[str] = None  # 게임 타입 추가 (선택적)
    game_state: Optional[GameState] = None  # 게임 상태 추가 (선택적)
    status: Optional[str] = "waiting"  # 방 상태 추가 (선택적)