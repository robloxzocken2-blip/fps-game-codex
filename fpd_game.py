"""A tiny first-person dungeon (FPD) game built with pygame.

Run:
    python fpd_game.py

Controls:
    W/S: move forward/backward
    A/D: strafe left/right
    Left/Right arrows: turn
    ESC or window close: quit
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import pygame

# Screen configuration
WIDTH, HEIGHT = 960, 600
HALF_HEIGHT = HEIGHT // 2
FPS = 60

# Player and world configuration
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 18
DELTA_ANGLE = FOV / NUM_RAYS
DIST_TO_PLANE = (WIDTH / 2) / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

MOVE_SPEED = 3.2
ROT_SPEED = 2.0

WORLD_MAP = [
    "111111111111",
    "100000000001",
    "101111011101",
    "100001000001",
    "101101110101",
    "100100010001",
    "101111010101",
    "100000000001",
    "111111111111",
]

MAP_WIDTH = len(WORLD_MAP[0])
MAP_HEIGHT = len(WORLD_MAP)


@dataclass
class Player:
    x: float = 2.5
    y: float = 2.5
    angle: float = 0.0

    def move(self, dx: float, dy: float) -> None:
        next_x = self.x + dx
        next_y = self.y + dy
        if not is_wall(next_x, self.y):
            self.x = next_x
        if not is_wall(self.x, next_y):
            self.y = next_y


def is_wall(x: float, y: float) -> bool:
    ix, iy = int(x), int(y)
    if ix < 0 or iy < 0 or ix >= MAP_WIDTH or iy >= MAP_HEIGHT:
        return True
    return WORLD_MAP[iy][ix] == "1"


def cast_rays(screen: pygame.Surface, player: Player) -> None:
    start_angle = player.angle - HALF_FOV

    for ray in range(NUM_RAYS):
        ray_angle = start_angle + ray * DELTA_ANGLE
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        depth = 0.02
        hit = False
        wall_x, wall_y = player.x, player.y

        while depth < MAX_DEPTH:
            wall_x = player.x + depth * cos_a
            wall_y = player.y + depth * sin_a
            if is_wall(wall_x, wall_y):
                hit = True
                break
            depth += 0.02

        if not hit:
            depth = MAX_DEPTH

        corrected_depth = depth * math.cos(player.angle - ray_angle)
        corrected_depth = max(corrected_depth, 0.0001)

        wall_height = min(int(DIST_TO_PLANE / corrected_depth), HEIGHT * 2)

        shade = max(20, 220 - int(corrected_depth * 14))
        color = (shade, shade // 2, shade // 3)

        x = ray * SCALE
        y = HALF_HEIGHT - wall_height // 2
        pygame.draw.rect(screen, color, (x, y, SCALE + 1, wall_height))


def draw_background(screen: pygame.Surface) -> None:
    # Sky
    pygame.draw.rect(screen, (85, 160, 235), (0, 0, WIDTH, HALF_HEIGHT))
    # Floor gradient-ish bands
    pygame.draw.rect(screen, (55, 50, 45), (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
    pygame.draw.rect(screen, (45, 40, 35), (0, HALF_HEIGHT + HALF_HEIGHT // 3, WIDTH, HALF_HEIGHT))


def handle_movement(player: Player, dt: float) -> None:
    keys = pygame.key.get_pressed()

    move_step = MOVE_SPEED * dt
    rot_step = ROT_SPEED * dt

    if keys[pygame.K_LEFT]:
        player.angle -= rot_step
    if keys[pygame.K_RIGHT]:
        player.angle += rot_step

    sin_a = math.sin(player.angle)
    cos_a = math.cos(player.angle)

    if keys[pygame.K_w]:
        player.move(cos_a * move_step, sin_a * move_step)
    if keys[pygame.K_s]:
        player.move(-cos_a * move_step, -sin_a * move_step)
    if keys[pygame.K_a]:
        player.move(sin_a * move_step, -cos_a * move_step)
    if keys[pygame.K_d]:
        player.move(-sin_a * move_step, cos_a * move_step)


def draw_hud(screen: pygame.Surface, clock: pygame.time.Clock, player: Player, font: pygame.font.Font) -> None:
    fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (245, 245, 245))
    pos_text = font.render(f"Pos: ({player.x:.2f}, {player.y:.2f})", True, (245, 245, 245))
    screen.blit(fps_text, (16, 12))
    screen.blit(pos_text, (16, 36))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FPD Python Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)

    player = Player()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        handle_movement(player, dt)
        draw_background(screen)
        cast_rays(screen, player)
        draw_hud(screen, clock, player, font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
