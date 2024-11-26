from typing import List, Dict, Optional

def initialize_game(players: List[str]) -> Dict:
    """
    게임 상태 초기화
    """
    return {
        "players": {index: {"name": player, "chips": 30, "card": None} for index, player in enumerate(players)},
        "current_turn": 0,
        "pot": 0,
        "round_completed": False
    }

def handle_action(state: Dict, player_index: int, action: str, bet_amount: Optional[int] = 0) -> Dict:
    """
    플레이어 행동 처리
    """
    if player_index != state["current_turn"]:
        return {"error": "Not your turn"}
    
    if action == "check":
        pass  # Check 로직
    elif action == "bet":
        if bet_amount <= 0:
            return {"error": "Bet amount must be greater than zero"}
        state["pot"] += bet_amount
    elif action == "fold":
        state["round_completed"] = True
        state["winner"] = 1 - player_index
    elif action == "raise":
        state["pot"] += bet_amount
    elif action == "call":
        state["round_completed"] = True
    else:
        return {"error": "Invalid action"}

    # 턴 변경
    state["current_turn"] = 1 - player_index
    return state

def reveal_winner(state: Dict) -> Dict:
    """
    카드 공개 및 승자 계산
    """
    if not state["round_completed"]:
        return {"error": "Round not completed"}

    # 각 플레이어의 카드를 랜덤으로 할당 (1 ~ 10)
    import random
    for player in state["players"].values():
        if player["card"] is None:
            player["card"] = random.randint(1, 10)
    
    players = state["players"]
    winner = max(players.items(), key=lambda x: x[1]["card"])[0]
    state["winner"] = winner
    return {"winner": winner}
