<script>
  import { onMount } from "svelte";
  import { fetchRooms, createRoom } from "../api";
  import { navigate } from "svelte-routing";

  let rooms = [];
  let newRoomId = "";
  let playerName = "";

  async function loadRooms() {
  try {
    const result = await fetchRooms();
    console.log("Fetched rooms:", result); // 응답 데이터 확인
    rooms = Array.isArray(result) ? result : [];
  } catch (err) {
    console.error("Failed to load rooms:", err);
    alert("Failed to load rooms.");
    rooms = [];
  }
}


  async function handleCreateRoom() {
    if (!newRoomId || !playerName) {
      alert("Room ID and Player Name are required.");
      return;
    }

    try {
      await createRoom(newRoomId);
      navigate(`/room/${newRoomId}?playerName=${encodeURIComponent(playerName)}`);
    } catch (err) {
      console.error("Failed to create room:", err);
      alert("Failed to create room.");
    }
  }

  onMount(() => {
    loadRooms();
  });
</script>

<div>
  <h2>Available Rooms</h2>
  <ul>
    {#each rooms as room (room.room_id)}
      <li>
        {room.room_id} (Players: {room.players ? room.players.length : 0}/2)
        <button on:click={() => navigate(`/room/${room.room_id}?playerName=${encodeURIComponent(playerName)}`)}>
          Join
        </button>
      </li>
    {/each}
  </ul>

  <h2>Create Room</h2>
  <input bind:value={newRoomId} placeholder="Room ID" />
  <input bind:value={playerName} placeholder="Your Name" />
  <button on:click={handleCreateRoom}>Create Room</button>
</div>
