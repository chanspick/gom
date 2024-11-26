const API_URL = "http://127.0.0.1:8000";

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

export async function fetchRooms() {
  const response = await fetch(`${API_URL}/rooms`);
  if (!response.ok) throw new Error("Failed to fetch rooms");
  return response.json();
}

export async function createRoom(roomId) {
  const response = await fetch(`${API_URL}/rooms`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ room_id: roomId }),
  });
  if (!response.ok) throw new Error("Failed to create room");
  return response.json();
}

export async function joinRoom(roomId, playerName) {
  return await safeFetch(`${API_URL}/rooms/${roomId}/join`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_name: playerName }),
  });
}

export async function getRoomState(roomId) {
  return await safeFetch(`${API_URL}/rooms/${roomId}/state`);
}

export async function startGame() {
  return await safeFetch(`${API_URL}/game_1/start_game`, {
    method: "POST",
  });
}

export async function playerAction(playerIndex, action, betAmount = 0) {
  return await safeFetch(`${API_URL}/game_1/player_action`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ player_index: playerIndex, action, bet_amount: betAmount }),
  });
}

export async function revealCards() {
  return await safeFetch(`${API_URL}/game_1/reveal_cards`, {
    method: "POST",
  });
}
