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

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors):
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        print("PRINTING ENTITIES")
        print(self.game_map.entities)
        print("PRINTING ACTORS")
        print(self.game_map.actors)
        for entity in set(self.game_map.actors):
            if True:  # entity.visible
                try:
                    entity.visible[:] = compute_fov(
                        self.game_map.tiles["transparent"],
                        (entity.x, entity.y),
                        radius=8,
                    )
                    # If a tile is "visible" it should be added to "explored".
                    entity.explored |= entity.visible
                    # Add to Uniqe Render
                    print("BIGGGGGGGGGGGGGGGGGgg")
                    print(entity.id)
                    self.unique_messages[entity.id] = entity.visible

                except exceptions.Impossible:
                    print("EPIC FAIL FIAFLAALLAF A")
                    pass  # Ignore impossible action exceptions from FOV

    def insert_actor(self, actor: Actor):
        self.game_map.entities.add(actor)

    def unique_render(self, id):
        print("PRINTING UNIQUE MESSAGES")
        print(self.unique_messages)
        print("PRINT DONE")
        return self.unique_messages[id]

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            #  current_value=self.player.fighter.hp,
            #  maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47),
        )

        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
