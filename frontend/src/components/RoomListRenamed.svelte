<script>
  import { onMount } from "svelte";
  import { fetchRooms, createRoom, joinRoom } from "../api";
  import { navigate } from "svelte-routing";

  let rooms = []; // 방 목록
  let roomId = ""; // 새 방 ID
  let playerName = ""; // 플레이어 이름
  let selectedGame = "indian-poker"; // 기본 선택된 게임
  let isCreatingRoom = false; // 방 생성 중 여부

  // 방 목록 불러오기
  async function loadRooms() {
    try {
      const result = await fetchRooms();
      rooms = Array.isArray(result) ? result : [];
    } catch (err) {
      console.error("Failed to load rooms:", err);
      alert("Failed to load rooms.");
    }
  }

  // 방 생성 함수
  async function handleCreateRoom() {
    if (isCreatingRoom) {
      return; // 이미 방 생성 요청이 진행 중이면 아무 동작도 하지 않음
    }

    if (!roomId.trim() || !playerName.trim()) {
      alert("Room ID, Game Type, and Player Name are required.");
      return;
    }

    try {
      isCreatingRoom = true;
      const response = await createRoom({
        room_id: roomId,
        game_type: selectedGame,
        player_name: playerName,
      });
      if (response.ok) {
        console.log(`Navigating to room: /room/${roomId}?playerName=${encodeURIComponent(playerName)}`);
        navigate(`/room/${roomId}?playerName=${encodeURIComponent(playerName)}`);
      } else {
        throw new Error("Failed to create room");
      }
    } catch (err) {
      console.error("Failed to create room:", err);
      alert("Failed to create room. Please try again.");
    } finally {
      isCreatingRoom = false;
    }
  }

  // 방 참여 함수
  async function handleJoinRoom(roomId) {
    if (!playerName.trim()) {
      alert("Player Name is required to join a room.");
      return;
    }

    try {
      const response = await joinRoom(roomId, playerName);
      if (response.ok) {
        console.log(`Navigating to room: /room/${roomId}?playerName=${encodeURIComponent(playerName)}`);
        navigate(`/room/${roomId}?playerName=${encodeURIComponent(playerName)}`);
      } else {
        throw new Error("Failed to join room");
      }
    } catch (err) {
      console.error("Failed to join room:", err);
      alert("Failed to join room. Please try again.");
    }
  }

  onMount(() => {
    loadRooms();
  });
</script>

<div class="container">
  <section>
    <h2>Available Rooms</h2>
    <input bind:value={playerName} placeholder="Your Name" class="join-player-name" />
    <ul class="room-list">
      {#if rooms.length > 0}
        {#each rooms as room (room.room_id)}
          <li class="room-item">
            <div class="room-details">
              <strong>{room.room_id}</strong>
              <span>Players: {room.players ? room.players.length : 0}/2</span>
            </div>
            <button
              class="join-button"
              on:click={() => handleJoinRoom(room.room_id)}
              disabled={room.players.length >= 2 || !playerName.trim()}
            >
              Join
            </button>
          </li>
        {/each}
      {:else}
        <p class="no-rooms">No rooms available. Create one to start!</p>
      {/if}
    </ul>
  </section>

  <section class="create-room">
    <h2>Create Room</h2>
    <input bind:value={roomId} placeholder="Enter Room ID" />
    <input bind:value={playerName} placeholder="Your Name" />

    <label for="gameType">Select Game:</label>
    <select bind:value={selectedGame} id="gameType">
      <option value="indian-poker">Indian Poker</option>
      <option value="new-game">New Game</option>
    </select>

    <button class="create-button" on:click={handleCreateRoom} disabled={isCreatingRoom}>Create Room</button>
  </section>
</div>

<style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
    padding: 20px;
  }

  h2 {
    margin-bottom: 15px;
    color: #333;
    text-align: center;
  }

  .room-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .room-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    background-color: #f9f9f9;
  }

  .room-details {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .room-details strong {
    font-size: 16px;
    color: #333;
  }

  .join-button {
    padding: 5px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .join-button:hover {
    background-color: #0056b3;
  }

  .join-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .no-rooms {
    text-align: center;
    color: #999;
    margin-top: 10px;
  }

  .create-room {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  input,
  select {
    padding: 10px;
    width: 100%;
    max-width: 300px;
    box-sizing: border-box;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  input:focus,
  select:focus {
    outline: none;
    border: 1px solid #007bff;
  }

  .create-button {
    align-self: center;
    padding: 10px 20px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .create-button:hover {
    background-color: #218838;
  }
</style>
