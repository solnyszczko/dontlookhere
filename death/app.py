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
from ulid import ULID
import json
import copy
import asyncio
import exceptions
import numpy as np
import pygame

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


magic_width = 100
magic_height = 100
my_engine = new_game()
event_handler = MainGameEventHandler(my_engine)
clock = pygame.time.Clock()


def input_handler(data, char_id):
    action = event_handler.ev_keydown(data, char_id)
    event_handler.handle_action(action)


def generate_character(id: str) -> Actor:
    player = copy.deepcopy(entity_factories.player)
    player.update_id(id)
    spawn_x = my_engine.game_map.cool_center[0] + random.randint(1, 2)
    spawn_y = my_engine.game_map.cool_center[1] + random.randint(1, 2)
    player.place(spawn_x, spawn_y, my_engine.game_map)

    return player


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        websocket.id = str(ULID())
        self.active_connections.append(websocket)

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
            await connection.send_json(my_engine.unique_render(connection.id))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def test():
    while True:
        #    clock.tick(1)
        await asyncio.sleep(1)
        print("asyncing")
        # game think
        #    my_engine.handle_enemy_turns()
        my_engine.update_fov()
        await manager.broadcast_unique_state()
        my_engine.get_target()
        my_engine.handle_enemy_turns()
        # game broadcast

    #   return None


@app.get("/")
async def get():
    pass
    # return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    websocket_id = websocket.id

    char = generate_character(websocket_id)
    my_engine.insert_actor(char)

    try:
        while True:
            data = await websocket.receive_text()
            input_handler(data, websocket_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    #   await manager.broadcast(f"Client #{client_id} left the chat")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(test())
