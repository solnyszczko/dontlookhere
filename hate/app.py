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
import copy

# import redis.asyncio as redis
import datetime
from entity import Actor
import entity_factories

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


active_players = dict()


def input_handler(data, id):
    if data == "up":
        active_players[str(id)]["y"] -= 1
    if data == "down":
        active_players[str(id)]["y"] += 1
    if data == "left":
        active_players[str(id)]["x"] -= 1
    if data == "right":
        active_players[str(id)]["x"] += 1


def generate_character(id):
    player = copy.deepcopy(entity_factories.player)
    player.id = id
    return player


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

        active_players[str(websocket.id)] = generate_character(str(websocket.id)).to_send()
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
    # return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast_game_state(list(active_players.values()))
    print("desu")
    try:
        while True:
            data = await websocket.receive_text()
            input_handler(data, websocket.id)
            await manager.broadcast_game_state(list(active_players.values()))
    #       await manager.send_personal_message(f"You wrote: {data}", websocket)
    #      await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
