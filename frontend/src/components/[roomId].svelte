<script>
    import { onMount } from "svelte"; // onMount를 import
    import { getRoomState } from "../api"; // 방 상태 가져오기 함수
  
    export let roomId; // 라우트에서 전달받은 roomId
  
    let roomState = {}; // 방 상태
  
    // 컴포넌트가 마운트될 때 실행
    onMount(async () => {
      try {
        roomState = await getRoomState(roomId); // 방 상태를 API로 가져옴
        console.log("Room state loaded:", roomState);
      } catch (err) {
        console.error("Failed to load room state:", err);
      }
    });
  </script>
  
  <h1>Room: {roomId}</h1>
  <p>Players in the room:</p>
  <ul>
    {#if roomState.players}
      {#each roomState.players as player}
        <li>{player.player_name}</li>
      {/each}
    {/if}
  </ul>
  