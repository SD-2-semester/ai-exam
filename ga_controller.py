from ga_model import SimpleModel
from snake import Snake, SnakeGame
from vector import Vector
import pygame
import numpy as np
from typing import Protocol
import math


class GameController(Protocol):
    def update(self) -> Vector:
        pass


class GAController(GameController):
    def __init__(self, game, model, display=False):
        self.game = game
        self.game.controller = self
        self.model: SimpleModel = model
        self.display = display
        self.fps = 24
        if self.display:
            pygame.init()
            self.screen = pygame.display.set_mode(
                (game.grid.x * game.scale, game.grid.y * game.scale)
            )
            self.clock = pygame.time.Clock()
            self.color_snake_head = (0, 255, 0)
            self.color_food = (255, 0, 0)
            self.font = pygame.font.Font(None, 36)
        self.action_space = (
            Vector(0, 1),
            Vector(0, -1),
            Vector(1, 0),
            Vector(-1, 0),
        )
        self.steps = 0

    def draw_score(self):
        score_text = f"Score: {self.game.snake.score}"  # Assuming `game.score` tracks the current score
        score_surf = self.font.render(score_text, True, (255, 255, 255))  # White color
        score_rect = score_surf.get_rect()
        score_rect.topleft = (10, 10)  # Position at top-left corner
        self.screen.blit(score_surf, score_rect)

    @property
    def score(self) -> int:
        return self.game.snake.score

    def calc_fitness(self) -> float:
        return self.score / (np.log(self.steps + 1))

    def update(self) -> Vector:

        obs = {}

        # danger left, right, up, down

        d_left, d_right, d_up, d_down = self.check_surrounding_danger()

        obs["danger_left"] = d_left
        obs["danger_right"] = d_right
        obs["danger_up"] = d_up
        obs["danger_down"] = d_down

        # direction left, right, up, down

        dir_left, dir_right, dir_up, dir_down = self.game.snake.direction

        obs["dir_left"] = dir_left
        obs["dir_right"] = dir_right
        obs["dir_up"] = dir_up
        obs["dir_down"] = dir_down

        # food relative position left right up down

        f_left, f_right, f_up, f_down = self.check_food_relative_position()

        obs["food_left"] = f_left
        obs["food_right"] = f_right
        obs["food_up"] = f_up
        obs["food_down"] = f_down

        obs = np.array(list(obs.values()))

        action = self.model.action(obs)
        next_move = self.action_space[action]
        try:
            if self.display:
                self.screen.fill("black")
                self.draw_score()
                for i, p in enumerate(self.game.snake.body):
                    pygame.draw.rect(
                        self.screen,
                        (0, max(128, 255 - i * 12), 0),
                        self.block(p),
                    )
                pygame.draw.rect(
                    self.screen, self.color_food, self.block(self.game.food.p)
                )
                pygame.display.flip()
                self.clock.tick(48)

            self.steps += 1
        except Exception as e:
            print(e)

        self.model.fitness = self.calc_fitness()
        return next_move

    def check_surrounding_danger(self) -> tuple[int, ...]:
        body = self.game.snake.body
        head = self.game.snake.p
        grid = self.game.grid

        dangers = [
            (head.x == 0 or (head + Vector(-1, 0)) in body),  # left
            (head.x == grid.x - 1 or (head + Vector(1, 0)) in body),  # right
            (head.y == 0 or (head + Vector(0, -1)) in body),  # up
            (head.y == grid.y - 1 or (head + Vector(0, 1)) in body),  # down
        ]

        return tuple(int(danger) for danger in dangers)

    def check_food_relative_position(self) -> tuple[int, ...]:
        head = self.game.snake.p
        food = self.game.food.p

        relative_position = [
            (head.x > food.x),  # left
            (head.x < food.x),  # right
            (head.y > food.y),  # up
            (head.y < food.y),  # down
        ]

        return tuple(int(position) for position in relative_position)

    @property
    def has_stopped(self) -> bool:
        return not self.game.running

    def block(self, obj):
        return (
            obj.x * self.game.scale,
            obj.y * self.game.scale,
            self.game.scale,
            self.game.scale,
        )

    def __del__(self):
        if self.display:
            pygame.quit()
