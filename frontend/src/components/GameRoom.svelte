<script>
  import { onMount } from "svelte";
  import GameBoard from "./GameBoard.svelte";
  import PlayerInfo from "./PlayerInfo.svelte";
  export let roomState; // roomState를 props로 받음
</script>

<div>
  {#if roomState && roomState.game_state !== null}
    <GameBoard gameState={roomState.game_state} />
    <div class="player-info-container">
      {#if roomState.players && roomState.players.length > 0}
        {#each roomState.players as player (player)}
          <PlayerInfo {player} />
        {/each}
      {:else}
        <p>Waiting for players...</p>
      {/if}
    </div>
  {:else if roomState && roomState.players.length === 1}
    <p>Waiting for the second player to join...</p>
  {:else}
    <p>Game state is not initialized yet.</p>
  {/if}
</div>

<style>
  .player-info-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1rem;
  }
</style>
