const API_URL = "http://127.0.0.1:8000";

// 공통 fetch 함수로 에러 처리 및 응답 핸들링
async function safeFetch(url, options = {}) {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      const errorDetails = await response.json();
      console.error(`HTTP error: ${response.status}`, errorDetails);
      throw new Error(errorDetails.detail || "Unknown error");
    }
    return await response.json();
  } catch (err) {
    console.error("Fetch error:", err.message);
    throw new Error("Network error or invalid JSON response");
  }
}

// 방 목록 가져오기
export async function fetchRooms() {
  try {
    return await safeFetch(`${API_URL}/room/`);
  } catch (err) {
    console.error("Failed to fetch rooms:", err.message);
    throw err;
  }
}

// 방 생성하기
export async function createRoom(data) {
  try {
    return await safeFetch(`${API_URL}/room/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  } catch (err) {
    console.error("Failed to create room:", err.message);
    throw err;
  }
}

// 방에 참여하기
export async function joinRoom(roomId, playerName) {
  try {
    return await safeFetch(`${API_URL}/room/${roomId}/join`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ player_name: playerName }),
    });
  } catch (err) {
    console.error(`Failed to join room ${roomId}:`, err.message);
    throw err;
  }
}

// 특정 방의 상태 가져오기
export async function getRoomState(roomId) {
  try {
    return await safeFetch(`${API_URL}/room/${roomId}`);
  } catch (err) {
    console.error(`Failed to fetch state for room ${roomId}:`, err.message);
    throw err;
  }
}

// 방 삭제하기
export async function deleteRoom(roomId) {
  try {
    return await safeFetch(`${API_URL}/room/${roomId}`, {
      method: "DELETE",
    });
  } catch (err) {
    console.error(`Failed to delete room ${roomId}:`, err.message);
    throw err;
  }
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

export function connectToRoom(roomId) {
  const socket = new WebSocket(`ws://127.0.0.1:8000/room/${roomId}/ws`);

  socket.onopen = () => {
    console.log("Connected to WebSocket for room:", roomId);
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  socket.onclose = () => {
    console.log("WebSocket connection closed");
  };

  return socket;
}
