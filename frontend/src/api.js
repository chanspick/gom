const API_URL = "http://127.0.0.1:8000";

// 공통 fetch 함수로 에러 처리 및 응답 핸들링
async function safeFetch(url, options = {}) {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      const errorDetails = await response.text();
      throw new Error(`HTTP error: ${response.status} - ${errorDetails}`);
    }
    return await response.json();
  } catch (err) {
    console.error("Fetch error:", err);
    throw new Error("Network error or invalid JSON response");
  }
}

// 방 목록 가져오기
export async function fetchRooms() {
  return await safeFetch(`${API_URL}/rooms/`);
}

// 방 생성하기
export async function createRoom(data) {
  return await safeFetch(`${API_URL}/rooms/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
}

// 방에 참여하기
export async function joinRoom(roomId, playerName) {
  return await safeFetch(`${API_URL}/rooms/${roomId}/join`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_name: playerName }),
  });
}

// 특정 방의 상태 가져오기
export async function getRoomState(roomId) {
  return await safeFetch(`${API_URL}/rooms/${roomId}`);
}

// 방 삭제하기
export async function deleteRoom(roomId) {
  return await safeFetch(`${API_URL}/rooms/${roomId}`, {
    method: "DELETE",
  });
}

// 게임 시작하기
export async function startGame() {
  return await safeFetch(`${API_URL}/game_1/start_game`, {
    method: "POST",
  });
}

// 플레이어의 행동 (check, bet, fold 등)
export async function playerAction(action, betAmount = 0) {
  return await safeFetch(`${API_URL}/game_1/player_action`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action, bet_amount: betAmount }),
  });
}

// 라운드 후 카드 공개
export async function revealCards() {
  return await safeFetch(`${API_URL}/game_1/reveal_cards`, {
    method: "POST",
  });
}
