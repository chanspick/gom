<script context="module">
  export async function load({ params }) {
    return { props: { roomId: params.roomId } };
  }
</script>

<script>
  import { onMount } from "svelte";
  import { getRoomState } from "../api"; // API 함수

  export let roomId;
  let roomState = { players: [] }; // 초기 값 설정
  let isLoading = true; // 로딩 상태
  let error = ""; // 에러 메시지 저장

  async function loadRoomState() {
    try {
      const data = await getRoomState(roomId); // 방 상태 로드
      roomState = data || { players: [] }; // 기본값 설정
      isLoading = false;
    } catch (err) {
      error = "Failed to load room state.";
      console.error(error, err);
      isLoading = false;
    }
  }

  onMount(() => {
    loadRoomState();
  });
</script>

{#if isLoading}
  <p>Loading room data...</p>
{:else if error}
  <p class="error">{error}</p>
{:else}
  <div class="game-room">
    <h1>Room ID: {roomId}</h1>
    <p>Status: {roomState.status || "Unknown"}</p>
    <h2>Players</h2>
    <ul>
      {#if roomState.players.length > 0}
        {#each roomState.players as player}
          <li>{player.player_name}</li>
        {/each}
      {:else}
        <li>No players in the room.</li>
      {/if}
    </ul>
    <h2>Game State</h2>
    <pre>{JSON.stringify(roomState.game_state, null, 2)}</pre>
  </div>
{/if}

<style>
  .game-room {
    max-width: 800px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
    padding: 20px;
    text-align: center;
  }

  .error {
    color: red;
    font-weight: bold;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    margin: 5px 0;
  }
</style>
