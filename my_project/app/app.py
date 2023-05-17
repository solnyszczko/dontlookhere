from beanie import init_beanie
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, WebSocket, WebSocketDisconnect

from rich import inspect, print
from rich.console import Console
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Dict, List, Optional
from fastapi.staticfiles import StaticFiles
import random
import uuid
import jsonpickle
import json


from app.db import User, db
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
console = Console()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)


class Player:
    def __init__(self, name: str, x: int, y: int, z: int, id:str):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.id = id

# Set up the game state
game_state = {
    'players': {},
    'objects': {},
    'score': 0,
    # ... etc.
}

active_players = dict()

def input_handler(data,id):
    if data == "up":
        active_players[str(id)]["y"] -= 1
    if data == "down":
        active_players[str(id)]["y"] += 1
    if data == "left":
        active_players[str(id)]["x"]-= 1
    if data == "right":
        active_players[str(id)]["x"] += 1                        

def generate_character(id):
   # game_state["players"].update(Player(name = ("meow"+ str(id)), x = random.randint(1,10), y = random.randint(1,10), z = random.randint(1,10), id = str(id)).__dict__)
    return Player(name = ("meow"+ id), x = random.randint(1,10), y = random.randint(1,10), z = random.randint(1,10), id = id)
    print(game_state["players"])
    


    


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        websocket.id = uuid.uuid4()
        
        active_players[str(websocket.id)] = generate_character(str(websocket.id)).__dict__
        print(active_players)
     #   print(websocket.id)
      #  print(websocket.headers)
        
        self.active_connections.append(websocket)
        print(self.active_connections)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        active_players.pop(str(websocket.id))

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
    #return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast_game_state(list(active_players.values()))
    print("desu")
    try:
        while True:
            data = await websocket.receive_text()
            input_handler(data,websocket.id)
            await manager.broadcast_game_state(list(active_players.values()))
     #       await manager.send_personal_message(f"You wrote: {data}", websocket)
      #      await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


