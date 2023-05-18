
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status, WebSocket, WebSocketDisconnect



from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Dict, List, Optional
from fastapi.staticfiles import StaticFiles
import random
import uuid
import json
import redis
#import redis.asyncio as redis
import datetime

from pydantic import EmailStr

from redis_om import HashModel


class Player(HashModel):
    name: str
    x: int
    y: int
    z: int
    id:str
 #   time_created: datetime.date
 #   bio: Optional[str]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")



pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
red = redis.StrictRedis(connection_pool=pool)

red.flushdb()


active_players = dict()

def input_handler(data,id):
    if data == "up":
        red.hincrby(str(id), 'y',-1 ) 
    if data == "down":
        red.hincrby(str(id), 'y',1 ) 
    if data == "left":
        red.hincrby(str(id), 'x',-1 ) 
    if data == "right":
        red.hincrby(str(id), 'x',1 )                       

def generate_character(id):
    return Player(name = ("meow"+ id), x = random.randint(1,10), y = random.randint(1,10), z = random.randint(1,10), id = id)

def redis_gen_state():
    keys = red.keys('*')
    values = []
    # Retrieve values for each key
    for key in keys:
        print(key)
        value = red.hgetall(key)  # or r.hget(hash_key, field) for hash data structure
        values.append(value)
    print("MEOW")
    print(values)
    return values



class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        websocket.id = uuid.uuid4()
        
       # active_players[str(websocket.id)] = generate_character(str(websocket.id)).__dict__
        red.hmset(str(websocket.id), generate_character(str(websocket.id)).__dict__)
     #   print(active_players)
     #   print(websocket.id)
      #  print(websocket.headers)
        
        self.active_connections.append(websocket)
        print(self.active_connections)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        red.delete(str(websocket.id))

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
    await manager.broadcast_game_state(redis_gen_state())
    #BROADCAST INITIAL DATA
    print("desu")
    try: #CLIENT UPDATE LOOP
        while True:
            data = await websocket.receive_text()
            input_handler(data,websocket.id)
            await manager.broadcast_game_state(redis_gen_state())

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_game_state(redis_gen_state())


