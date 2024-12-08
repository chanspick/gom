export const IndianPokerLogic = {
  gameState: {
    pot: 0,
    myCard: "?",
    opponentCard: "?",
    currentTurn: null,
  },

  // 서버에서 받은 새로운 상태로 gameState를 업데이트
  updateState(newState) {
    this.gameState = {
      ...this.gameState,
      ...newState,
    };
  },

  // 캔버스 렌더링 메서드
  render(context, playerName) {
    // 캔버스 초기화
    context.clearRect(0, 0, 600, 400);

    // 게임 정보 렌더링
    context.font = "20px Arial";
    context.fillStyle = "black";

    context.fillText("Indian Poker", 20, 30);
    context.fillText(`Pot: ${this.gameState.pot}`, 20, 60);

    // 내 카드와 상대 카드
    context.fillText(`Your Card: ?`, 20, 90); // 자신의 카드는 항상 "?"로 표시
    context.fillText(
      `Opponent's Card: ${this.gameState.opponentCard || "?"}`,
      20,
      120
    );

    // 현재 턴 정보
    context.fillText(
      `Current Turn: ${
        this.gameState.currentTurn === playerName
          ? "Your Turn"
          : "Opponent's Turn"
      }`,
      20,
      150
    );
  },
};
