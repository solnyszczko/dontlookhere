from __future__ import annotations

from typing import TYPE_CHECKING
import lzma
import pickle
import numpy as np
from tcod.console import Console
from tcod.map import compute_fov

from message_log import MessageLog
import exceptions
import render_functions
import tile_types

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

    def get_target(self) -> None:
        distance = 100.0
        for entity in set(self.game_map.actors):
            for target in set(self.game_map.actors):
                if entity != target:
                    try:
                        x = entity.distance(target.x, target.y)
                        if x <= distance:
                            distance = x
                    except exceptions.Impossible:
                        print("COULD NOT GET_PLAYER")
                        pass  # Ignore impossible action exceptions from AI.
            entity.target = target.x, target.y

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

    def unique_render(self, id):  # console stuff
        print("PRINTING UNIQUE RENDER")

        meow = np.select(
            condlist=[self.unique_messages[id]],
            choicelist=[self.game_map.tiles["light"]],
            default=tile_types.SHROUD,
        )
        entities_sorted_for_rendering = sorted(
            self.game_map.entities, key=lambda x: x.render_order.value
        )

        desu = self.unique_messages[id]

        y = dict()
        y["visible"] = desu.tolist()
        for entity in entities_sorted_for_rendering:
            if desu[entity.x, entity.y]:
                print(entity.id)
                y[entity.id] = [entity.char, entity.x, entity.y]
        print(y)
        return y

    def render(self, console: Console) -> None:
        self.game_map.render(console)

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
