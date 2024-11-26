from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from .logic import initialize_game, handle_action, reveal_winner

router = APIRouter()

# 전역 데이터 (데모용)
game_states: Dict[str, Dict] = {}

# 요청 모델
class ActionRequest(BaseModel):
    player_index: int
    action: str
    bet_amount: Optional[int] = 0

@router.post("/start_game")
def start_game():
    """
    새로운 게임 시작
    """
    if "game_1" in game_states:
        raise HTTPException(status_code=400, detail="Game already started")
    game_states["game_1"] = initialize_game(["Player 1", "Player 2"])
    return {"message": "Game started", "state": game_states["game_1"]}

@router.post("/player_action")
def player_action(request: ActionRequest):
    """
    플레이어 행동 처리
    """
    if "game_1" not in game_states:
        raise HTTPException(status_code=400, detail="Game not started")
    state = game_states["game_1"]
    result = handle_action(state, request.player_index, request.action, request.bet_amount)
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])
    return {"message": "Action processed", "state": state}

@router.post("/reveal_cards")
def reveal_cards():
    """
    카드 공개 및 승자 결정
    """
    if "game_1" not in game_states:
        raise HTTPException(status_code=400, detail="Game not started")
    state = game_states["game_1"]
    result = reveal_winner(state)
    return {"message": "Winner revealed", "winner": result["winner"], "state": state}
