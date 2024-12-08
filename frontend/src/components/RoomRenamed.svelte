<script context="module">
  export async function load({ params }) {
    return { props: { roomId: params.roomId } };
  }
</script>

<script>
  import { onMount } from "svelte";
  import { getRoomState } from "../api"; // API 함수
  import GameCanvas from "./GameCanvas.svelte"; // 캔버스 컴포넌트

  export let roomId;
  let roomState = { players: [], game_state: null }; // 초기값 설정
  let selectedGameLogic = null; // 선택된 게임 로직
  let isLoading = true; // 로딩 상태
  let error = ""; // 에러 메시지

  // 동적으로 게임 로직 가져오기
  async function loadGameLogic(gameType) {
    try {
      const module = await import(`../gameLogics/${gameType}.js`);
      return module.default;
    } catch (err) {
      console.error(`Failed to load game logic for type: ${gameType}`, err);
      return null;
    }
  }

  // 방 상태와 게임 로직 로드
  async function loadRoomState() {
    try {
      const data = await getRoomState(roomId); // API에서 방 상태 가져오기
      roomState = data || { players: [] };
      selectedGameLogic = await loadGameLogic(roomState.game_type || "default");
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
      {#each roomState.players as player}
        <li>{player.player_name}</li>
      {/each}
    </ul>
    <h2>Game State</h2>
    <pre>{JSON.stringify(roomState.game_state, null, 2)}</pre>

    <div class="canvas-container">
      <GameCanvas {roomState} {roomId} {selectedGameLogic} />
    </div>
  </div>
{/if}

<style>
  /* 기존 스타일 유지 */
</style>
