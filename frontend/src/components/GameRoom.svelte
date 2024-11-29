<script>
  import GameCanvas from "./GameCanvas.svelte";

  // 방 상태와 게임 로직을 props로 전달받음
  export let roomState; // 방 상태
  export let selectedGameLogic; // 선택된 게임 로직
  export let roomId; 
</script>

<div class="room-container">
  <!-- 플레이어 정보 섹션 -->
  <div class="player-info-container">
    {#if roomState.players && roomState.players.length > 0}
      {#each roomState.players as player (player.name)}
        <div class="player-info">
          <h3>{player.name}</h3>
          <p>Chips: {player.chips}</p>
        </div>
      {/each}
    {:else}
      <p>플레이어를 기다리는 중...</p>
    {/if}
  </div>

  <!-- 게임 캔버스 -->
  <GameCanvas {roomState} {selectedGameLogic} {roomId}/>
</div>

<style>
  .room-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
  }

  .player-info-container {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    width: 100%;
    max-width: 600px;
  }

  .player-info {
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    flex: 1;
  }

  h3 {
    margin: 0;
  }

  p {
    margin: 5px 0 0;
  }
</style>
