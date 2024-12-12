<!-- src/components/GameCanvas.svelte -->
<script lang="ts">
  import { onMount } from "svelte";

  // TypeScript 인터페이스 정의
  interface Player {
    player_name: string;
  }

  interface GameState {
    players: { [key: string]: { chips: number; card: string | null } };
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

  export let roomState: RoomState;
  export let selectedGameLogic: any;

  let canvas: HTMLCanvasElement;
  let context: CanvasRenderingContext2D | null;

  // 캔버스 렌더링 함수
  function drawCanvas(state: GameState | null) {
    if (
      selectedGameLogic &&
      typeof selectedGameLogic.render === "function" &&
      context
    ) {
      selectedGameLogic.render(context, state);
    } else {
      console.warn("Selected game logic is invalid or not set.");
    }
  }

  // roomState가 변경될 때마다 캔버스 다시 그리기
  $: {
    const currentState = roomState.game_state;
    drawCanvas(currentState);
  }

  onMount(() => {
    context = canvas.getContext("2d");
    if (!context) {
      console.error("Failed to get canvas context.");
      return;
    }

    drawCanvas(roomState.game_state);
  });
</script>

<canvas
  bind:this={canvas}
  width="600"
  height="400"
  style="border: 1px solid black; background-color: #f9f9f9; border-radius: 8px;"
></canvas>
