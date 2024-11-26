<script>
  import { onMount } from "svelte";
  import { getRoomState, joinRoom } from "../api";
  import GameRoom from "./GameRoom.svelte";

  export let roomId; // 상위 컴포넌트 또는 라우트에서 전달되는 roomId
  let roomState = null;
  let playerName = "";

  // 디버깅용 roomId 확인
  console.log("roomId:", roomId);

  async function loadRoomState() {
    try {
      const urlParams = new URLSearchParams(window.location.search);
      playerName = urlParams.get("playerName") || localStorage.getItem("playerName");

      if (!playerName) {
        alert("Player name is required.");
        return;
      }

      localStorage.setItem("playerName", playerName);

      await joinRoom(roomId, playerName);
      const result = await getRoomState(roomId);
      console.log("Room state after join:", result);
      roomState = { ...result };
    } catch (error) {
      console.error("Error loading room state:", error);
    }
  }

  onMount(() => {
    if (!roomId) {
      console.error("Room ID is missing");
      alert("Room ID is missing. Please try again.");
      return;
    }
    loadRoomState();
  });
</script>

<div>
  <h1>Room: {roomId}</h1>
  {#if roomState}
    <GameRoom {roomState} />
  {:else}
    <p>Loading...</p>
  {/if}
</div>
