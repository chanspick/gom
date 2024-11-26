from pydantic import BaseModel

class Room(BaseModel):
    room_id: str
    players: list
    game_started: bool

class Player(BaseModel):
    player_name: str
    chips: int

class GameState(BaseModel):
    current_turn: int
    pot: int
    round_completed: bool
