<script>
  import { onMount, onDestroy } from "svelte";

  export let roomState;
  export let selectedGameLogic;
  export let roomId;

  let canvas;
  let context;
  let socket;

  // 캔버스 렌더링 함수
  function drawCanvas() {
    if (
      selectedGameLogic &&
      typeof selectedGameLogic.render === "function" &&
      context
    ) {
      selectedGameLogic.render(context, roomState);
    } else {
      console.warn("Selected game logic is invalid or not set.");
    }
  }

  // WebSocket 초기화
  function connectWebSocket() {
    socket = new WebSocket(`ws://localhost:8000/room/${roomId}/ws`);

    socket.onopen = () => {
      console.log("WebSocket connection established");
    };

    socket.onmessage = (event) => {
      const updatedState = JSON.parse(event.data);
      roomState = updatedState; // 상태 업데이트
      drawCanvas(); // 캔버스 다시 그리기
    };

    socket.onclose = (event) => {
      console.warn("WebSocket connection closed:", event.reason);
      // 일정 시간 후 재연결
      setTimeout(() => connectWebSocket(), 5000);
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  onMount(() => {
    context = canvas.getContext("2d");
    if (!context) {
      console.error("Failed to get canvas context.");
      return;
    }

    connectWebSocket();
    drawCanvas();
  });

  onDestroy(() => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.close();
      console.log("WebSocket connection closed on component destroy.");
    }
    context = null;
  });
</script>

<canvas
  bind:this={canvas}
  width="600"
  height="400"
  style="border: 1px solid black; background-color: #f9f9f9; border-radius: 8px;"
></canvas>
