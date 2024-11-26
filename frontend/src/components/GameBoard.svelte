<script>
  export let gameState = { current_turn: "N/A" }; // 기본값 제공

  function handleAction(action) {
    console.log(`Player performed: ${action}`);
    // Handle action logic
  }
</script>

<div>
  <h2>Game Board</h2>
  {#if gameState}
    <p>Current Turn: {gameState.current_turn}</p>
    <button on:click={() => handleAction("check")}>Check</button>
    <button on:click={() => handleAction("bet")}>Bet</button>
    <button on:click={() => handleAction("fold")}>Fold</button>
  {:else}
    <p>Game state is not available.</p>
  {/if}
</div>
