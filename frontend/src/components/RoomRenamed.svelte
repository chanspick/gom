<!-- src/routes/Room.svelte -->
<script lang="ts" context="module">
  export async function load({ params }) {
    return { props: { roomId: params.roomId } };
  }
</script>

<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { getRoomState, joinRoom, connectToRoom } from "../api"; // API 함수
  import GameCanvas from "./GameCanvas.svelte"; // 캔버스 컴포넌트
  import { writable } from 'svelte/store';

  export let roomId: string;

  // TypeScript 인터페이스 정의
  interface Player {
    player_name: string;
  }

  interface PlayerData {
    chips: number;
    card: string | null;
  }

  interface GameState {
    players: { [key: string]: PlayerData };
    current_turn: string;
    pot: number;
    round_completed: boolean;
    game_round: number;
    winner: string | null;
  }

  interface RoomState {
    room_id: string;
    game_type: string;
    players: Player[];
    game_started: boolean;
    game_state: GameState | null;
    status: string;
  }

  // Svelte Store로 방 상태 관리
  let roomState = writable<RoomState>({
    room_id: "",
    game_type: "",
    players: [],
    game_started: false,
    game_state: null,
    status: "unknown"
  });

  let selectedGameLogic: any = null; // 선택된 게임 로직
  let isLoading = true; // 로딩 상태
  let error = ""; // 에러 메시지
  let playerName = ""; // 플레이어 이름 입력
  let isJoined = false; // 방 참여 여부
  let socket: WebSocket; // WebSocket 인스턴스

  // 동적으로 게임 로직 가져오기
  async function loadGameLogic(gameType: string) {
    try {
      const module = await import(`../gameLogics/${gameType}.js`);
      return module.default;
    } catch (err) {
      console.error(`Failed to load game logic for type: ${gameType}`, err);
      return null;
    }
  }

  // 초기 방 상태 로드
  async function loadInitialRoomState() {
    try {
      const data: RoomState = await getRoomState(roomId); // API에서 방 상태 가져오기
      roomState.set(data || {
        room_id: roomId,
        game_type: "default",
        players: [],
        game_started: false,
        game_state: null,
        status: "unknown"
      });
      selectedGameLogic = await loadGameLogic(data.game_type || "default");
      isLoading = false;
      // 방 생성자나 이미 참여한 플레이어인지 확인
      if (data.players.some(p => p.player_name === playerName)) {
        isJoined = true;
      }
    } catch (err) {
      error = "Failed to load room state.";
      console.error(error, err);
      isLoading = false;
    }
  }

  // WebSocket 메시지 핸들러
  function handleWebSocketMessage(data: any) {
    if (data.type === "room_deleted") {
      alert(`Room ${data.room_id} has been deleted.`);
      // 필요한 경우 리디렉션 처리
      window.location.href = '/';
      return;
    }
    roomState.set(data); // 상태 업데이트
    // 선택된 게임 로직이 변경된 경우 다시 로드
    if (data.game_type && data.game_type !== selectedGameLogic?.game_type) {
      loadGameLogic(data.game_type).then(logic => {
        selectedGameLogic = logic;
      });
    }
  }

  // WebSocket 열림 핸들러
  function handleWebSocketOpen(socketInstance: WebSocket) {
    console.log("WebSocket connection established in Room.svelte");
  }

  // WebSocket 닫힘 핸들러
  function handleWebSocketClose(event: CloseEvent) {
    console.warn("WebSocket connection closed in Room.svelte:", event.reason);
    // 일정 시간 후 재연결 시도
    setTimeout(() => {
      socket = connectToRoom(roomId, handleWebSocketMessage, handleWebSocketOpen, handleWebSocketClose, handleWebSocketError);
    }, 5000);
  }

  // WebSocket 에러 핸들러
  function handleWebSocketError(error: Event) {
    console.error("WebSocket error in Room.svelte:", error);
  }

  onMount(() => {
    loadInitialRoomState();
    // WebSocket 연결
    socket = connectToRoom(roomId, handleWebSocketMessage, handleWebSocketOpen, handleWebSocketClose, handleWebSocketError);
  });

  onDestroy(() => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.close();
      console.log("WebSocket connection closed on component destroy in Room.svelte.");
    }
  });
</script>

{#if isLoading}
  <p>Loading room data...</p>
{:else if error}
  <p class="error">{error}</p>
{:else}
  <div class="game-room">
    <h1>Room ID: {roomId}</h1>
    <p>Status: {$roomState.status || "Unknown"}</p>
    <h2>Players</h2>
    <ul>
      {#each $roomState.players as player}
        <li>{player.player_name}</li>
      {/each}
    </ul>

    {#if isJoined}
      <h2>Game State</h2>
      <pre>{JSON.stringify($roomState.game_state, null, 2)}</pre>

      <div class="canvas-container">
        <GameCanvas selectedGameLogic={selectedGameLogic} roomState={$roomState} />
      </div>
    {/if}
  </div>
{/if}

<style>
  .game-room {
    padding: 20px;
  }

  .error {
    color: red;
  }

  .canvas-container {
    margin-top: 20px;
  }
</style>
