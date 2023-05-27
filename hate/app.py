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
import asyncio
import tcod

# import redis.asyncio as redis
import datetime
from entity import Actor
import entity_factories
from game_map import GameWorld
from input_handlers import MainGameEventHandler
from actions import BumpAction
from setup_game import new_game

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

my_engine = new_game()
event_handler = MainGameEventHandler(my_engine)


def input_handler(data, char_id):
    if data == "up":
        event_handler.ev_keydown(data, char_id)
        print("WENT UP")
        # action.perform and event handler maingameeventhandler
    if data == "down":
        event_handler.ev_keydown(data, char_id)
    if data == "left":
        event_handler.ev_keydown(data, char_id)
    if data == "right":
        event_handler.ev_keydown(data, char_id)


def generate_character(id: str) -> Actor:
    player = copy.deepcopy(entity_factories.player)
    player.update_id(id)
    player.update_loc()
    #   print(vars(player))
    return player


test_player = generate_character("test")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        websocket.id = uuid.uuid4()

        self.active_connections.append(websocket)
        print(self.active_connections)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_game_state(self, message_dict: dict, websocket: WebSocket):
        await websocket.send_json(message_dict)

    async def broadcast_game_state(self, message_dict: dict):
        for connection in self.active_connections:
            await connection.send_json(message_dict)

    async def broadcast_unique_state(self):
        for connection in self.active_connections:
            websocket_id = str(connection.id)
            await connection.send_json((my_engine.unique_render(websocket_id)).tolist())

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def test():
    while True:
        await asyncio.sleep(1)
        print("asyncing")
        # game think
        my_engine.update_fov()
        # game broadcast
        await manager.broadcast_unique_state()

    #   return None


@app.get("/")
async def get():
    pass
    # return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    websocket_id = str(websocket.id)
    char = generate_character(websocket_id)
    #   print(vars(char))
    my_engine.insert_actor(char)

    print("desu")
    try:
        while True:
            data = await websocket.receive_text()
            input_handler(data, websocket_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(test())
