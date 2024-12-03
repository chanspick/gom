<script>
  import { onMount } from "svelte";
  import { fetchRooms, createRoom, joinRoom } from "../api";

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
    if (!roomId.trim() || !playerName.trim()) {
      alert("Room ID and Player Name are required.");
      return;
    }

    try {
      isCreatingRoom = true;
      const response = await createRoom({
        room_id: roomId,
        game_type: selectedGame,
        player_name: playerName,
      });
      if (response) {
        console.log(`Navigating to /room/${roomId}`);
        window.location.href = `/room/${roomId}`;
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
      if (response) {
        console.log(`Navigating to /room/${roomId}`);
        window.location.href = `/room/${roomId}`;
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
  <!-- 방 목록 섹션 -->
  <section>
    <h2>Available Rooms</h2>
    <input
      bind:value={playerName}
      placeholder="Enter Your Name"
      class="player-name-input"
    />

    <ul class="room-list">
      {#if rooms.length > 0}
        {#each rooms as room (room.room_id)}
          <li class="room-item">
            <div>
              <strong>Room ID:</strong> {room.room_id} <br />
              <strong>Game:</strong> {room.game_type} <br />
              <strong>Status:</strong> {room.status} <br />
              <strong>Players:</strong> {room.players.join(", ")}
            </div>
            <button
              on:click={() => handleJoinRoom(room.room_id)}
              disabled={room.players.length >= 2 || !playerName.trim()}
            >
              Join
            </button>
          </li>
        {/each}
      {:else}
        <p class="no-rooms">No rooms available. Create one to get started!</p>
      {/if}
    </ul>
  </section>

  <!-- 방 생성 섹션 -->
  <section class="create-room">
    <h2>Create Room</h2>
    <input bind:value={roomId} placeholder="Room ID" />
    <input bind:value={playerName} placeholder="Your Name" />
    <select bind:value={selectedGame}>
      <option value="indian-poker">Indian Poker</option>
      <option value="new-game">New Game</option>
    </select>
    <button on:click={handleCreateRoom} disabled={isCreatingRoom}>
      Create Room
    </button>
  </section>
</div>

<style>
  .container {
    max-width: 600px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
    padding: 20px;
  }

  h2 {
    text-align: center;
    margin-bottom: 20px;
  }

  input,
  select {
    display: block;
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  .player-name-input {
    margin-bottom: 20px;
  }

  .room-list {
    list-style: none;
    padding: 0;
  }

  .room-item {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .create-room {
    margin-top: 30px;
  }

  .no-rooms {
    text-align: center;
    color: #777;
  }
</style>
