from random import randint
from core.models import Player, GameState
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    """
    플레이어 간의 WebSocket 연결을 관리합니다.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# 전역 상태: 게임 상태를 전역적으로 관리
state = GameState(players=[Player(name="Player 1"), Player(name="Player 2")])

# 게임 초기화 함수
def start_game():
    """
    게임을 초기화하고 플레이어들에게 칩과 카드를 랜덤하게 부여합니다.
    """
    # 각 플레이어 초기화
    for player in state.players:
        player.chips = 30  # 기본 칩 30개
        player.card = randint(1, 10)  # 카드 1~10 랜덤 부여

    # 첫 번째 플레이어 무작위로 지정
    state.current_turn = randint(0, 1)
    state.pot = 0  # 배팅 금액 초기화
    state.round_completed = False
    return {"message": "Game started", "state": state}


def player_action(player_index: int, action: str, bet_amount: int = 0):
    """
    플레이어의 행동(Check, Bet, Fold 등)을 처리합니다.
    """
    if state.round_completed:
        return {"error": "Round is already completed"}

    # 현재 턴인지 확인
    if player_index != state.current_turn:
        return {"error": "Not your turn"}

    # 플레이어와 상대방 설정
    player = state.players[player_index]
    opponent = state.players[1 - player_index]

    # 행동 처리
    if action == "check":
        # 턴을 상대방에게 넘김
        state.current_turn = 1 - state.current_turn

    elif action == "bet":
        # 칩 부족 확인
        if bet_amount > player.chips:
            return {"error": "Not enough chips to bet"}
        # 베팅 처리
        player.chips -= bet_amount
        state.pot += bet_amount
        state.current_turn = 1 - state.current_turn

    elif action == "fold":
        # 포기 시 상대방이 승리, 특수 규칙 적용
        if player.card == 10:
            opponent.chips += 10  # 10을 들고 포기하면 10칩을 상대에게 줌
        else:
            opponent.chips += state.pot
        state.round_completed = True  # 라운드 종료

    elif action == "raise":
        # 칩 부족 확인
        if bet_amount > player.chips:
            return {"error": "Not enough chips to raise"}
        # 레이즈 처리
        player.chips -= bet_amount
        state.pot += bet_amount
        state.current_turn = 1 - state.current_turn

    elif action == "call":
        # 콜 처리 후 라운드 종료
        state.round_completed = True

    else:
        return {"error": "Invalid action"}

    return {"message": f"Player {player_index} chose to {action}", "state": state}


def reveal_cards():
    """
    라운드 종료 후 각 플레이어의 카드를 공개하고 승자를 결정합니다.
    """
    if not state.round_completed:
        return {"error": "Round is not completed yet"}

    player1 = state.players[0]
    player2 = state.players[1]

    # 카드 비교하여 승자 결정
    if player1.card > player2.card:
        player1.chips += state.pot
        winner = player1.name
    elif player2.card > player1.card:
        player2.chips += state.pot
        winner = player2.name
    else:
        # 무승부 시 다음 판 기본 배팅에 사용
        winner = "Tie"

    # 상태 초기화
    state.pot = 0
    state.round_completed = False
    for player in state.players:
        player.card = None

    return {
        "message": "Round completed",
        "winner": winner,
        "state": state
    }
