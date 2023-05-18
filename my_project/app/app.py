from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    status,
    WebSocket,
    WebSocketDisconnect,
)


from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Dict, List, Optional
from fastapi.staticfiles import StaticFiles
import random
import uuid
import json
import redis

# import redis.asyncio as redis
import datetime

from pydantic import EmailStr

from redis_om import(
    HashModel,
    EmbeddedJsonModel,
    Field,
    JsonModel,
    Migrator,
    NotFoundError,
    QueryNotSupportedError,
    RedisModelError,
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


pool = redis.ConnectionPool(host="localhost", port=6379, db=0, decode_responses=True)
red = redis.StrictRedis(connection_pool=pool)

#red.flushdb()





class Player(HashModel):
    name: str
    x: int = random.randint(1, 10)
    y: int = random.randint(1, 10)
    z: int = random.randint(1, 10)
    id: str = Field(index=True)
    container_id: Optional[str]
 #   char: Optional[str] = ""
 #   join_date: datetime.date = (datetime.date.today(),)



def input_handler(data, id):
    if data == "up":
        Game_state.players[str(id)]["y"] -= 1
    if data == "down":
        Game_state.players[str(id)]["y"] += 1
    if data == "left":
        Game_state.players[str(id)]["x"] -= 1
    if data == "right":
        Game_state.players[str(id)]["x"] += 1


def generate_character(id):
    print(id)
    return Player(name="meow",id=id)
    


def generate_unique_state(id):
    # get_fov
    # aggregate visible objects
    # return
    pass

test_player = generate_character("test")




class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        websocket.id = uuid.uuid4()

        # red.hmset(str(websocket.id), generate_character(str(websocket.id)).__dict__)
        #   print(active_players)
        #   print(websocket.id)
        #  print(websocket.headers)

        self.active_connections.append(websocket)
        print(self.active_connections)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    #  red.delete(str(websocket.id))

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_game_state(self, message_dict: dict, websocket: WebSocket):
        await websocket.send_json(message_dict)

    async def broadcast_game_state(self, message_dict: dict):
        for connection in self.active_connections:
            await connection.send_json(message_dict)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
manager = ConnectionManager()




@app.get("/")
async def get():
    pass
    # return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    Game_state.players[str(websocket.id)] = generate_character(
        str(websocket.id)
    ).__dict__

    await manager.broadcast_game_state(list(Game_state.players.values()))
    # BROADCAST INITIAL DATA
    print("desu")
    try:  # CLIENT UPDATE LOOP
        while True:
            data = await websocket.receive_text()
            input_handler(data, websocket.id)
            await manager.broadcast_game_state(list(Game_state.players.values()))

    except WebSocketDisconnect:
        Game_state.players.pop(str(websocket.id))
        manager.disconnect(websocket)
        await manager.broadcast_game_state(list(Game_state.players.values()))
