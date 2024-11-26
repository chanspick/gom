<script>
  import { Router, Route } from "svelte-routing";
  import RoomList from "./components/RoomListRenamed.svelte";
  import Room from "./components/RoomRenamed.svelte";
</script>

<Router>
  <Route path="/" component={RoomList} />
  <Route path="/room/:roomId" component={Room} />
</Router>

