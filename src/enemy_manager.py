import math
from dataclasses import dataclass

import arcade

from src.consts import *
from src.vec import Vec2

SPAWN_DELAY = 10
RAGE_DELAY = 10
ENEMY_SPEED = 10

@dataclass
class Enemy:
    pos: Vec2
    dead: bool = False

class EnemyManager:
    def __init__(self, game):
        self.game = game

        self.enemies = []
        self.until_spawn = -5
        self.until_rage = RAGE_DELAY
        self.rage_mode = False

    def on_collision(self, enemy, player):
        if self.rage_mode:
            print("Enemy died")
            enemy.dead = True
        else:
            print("Player died")
            pass # TODO kill the player D:

    def update(self, dt):
        self.until_spawn -= dt
        if self.until_spawn < 0:
            self.until_spawn += SPAWN_DELAY
            self.enemies.append(Enemy(Vec2(2, 2))) # TODO select a better location
        self.until_rage -= dt
        if self.until_rage < 0:
            self.until_rage += RAGE_DELAY
            self.rage_mode = not self.rage_mode

        player = self.game.player
        for enemy in self.enemies:
            delta = player.pos - enemy.pos
            ln = delta.len()
            delta /= ln

            enemy_grid_x = int(enemy.pos.x / GRID_SCALE)
            enemy_grid_y = int(enemy.pos.y / GRID_SCALE)

            pathFindDir = Vec2(0.0, 0.0)

            if self.game.isXYInGrid(enemy_grid_x, enemy_grid_y):
                pathFindDir = self.game.pathFindingMap.gradient[enemy_grid_y * GRID_WIDTH + enemy_grid_x]

            direction = (delta*0.25 + pathFindDir).normalized()

            if self.rage_mode:
                direction *= -0.8

            enemy.pos += direction * ENEMY_SPEED * dt

            if ln < PLAYER_SIZE:
                self.on_collision(enemy, player)

        self.enemies[:] = [enemy for enemy in self.enemies if not enemy.dead]

    def draw(self):
        for enemy in self.enemies:
            arcade.draw_rectangle_filled(*enemy.pos, PLAYER_SIZE, PLAYER_SIZE, color=arcade.color.CRIMSON)