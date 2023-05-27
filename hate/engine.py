from __future__ import annotations

from typing import TYPE_CHECKING
import lzma
import pickle

from tcod.console import Console
from tcod.map import compute_fov

from message_log import MessageLog
import exceptions
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.unique_messages = dict()

    def get_player(self, id: str) -> Actor:
        for entity in set(self.game_map.actors):
            if entity.id == id:
                try:
                    return entity
                except exceptions.Impossible:
                    print("COULD NOT GET_PLAYER")
                    pass  # Ignore impossible action exceptions from AI.

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors):
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""

        for entity in set(self.game_map.actors):
            if True:  # entity.visible
                try:
                    visible = compute_fov(
                        self.game_map.tiles["transparent"],
                        (entity.x, entity.y),
                        radius=8,
                    )
                    # If a tile is "visible" it should be added to "explored".
                    #    entity.explored |= entity.visible
                    # Add to Uniqe Render
                    self.unique_messages[entity.id] = visible

                except exceptions.Impossible:
                    print("EPIC FAIL FIAFLAALLAF A")
                    pass  # Ignore impossible action exceptions from FOV

    def insert_actor(self, actor: Actor):
        self.game_map.entities.add(actor)

    def unique_render(self, id):
        print("PRINTING UNIQUE RENDER")
        print(self.unique_messages[id])
        return self.unique_messages[id]

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
