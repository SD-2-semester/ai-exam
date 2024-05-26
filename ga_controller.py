from game_controller import GameController
from snake import SnakeGame
from vector import Vector
import pygame
import numpy as np


class GAController(GameController):
    def __init__(self, game, model, display=False):
        self.game = game
        self.game.controller = self
        self.model = model
        self.display = display
        if self.display:
            pygame.init()
            self.screen = pygame.display.set_mode(
                (game.grid.x * game.scale, game.grid.y * game.scale)
            )
            self.clock = pygame.time.Clock()
            self.color_snake_head = (0, 255, 0)
            self.color_food = (255, 0, 0)
        self.action_space = (
            Vector(0, 1),
            Vector(0, -1),
            Vector(1, 0),
            Vector(-1, 0),
        )
        self.steps = 0

    @property
    def score(self) -> int:
        return self.game.snake.score

    @property
    def fitness(self) -> float:
        score = self.score
        return score / (np.log(self.steps + 1)) - 0.01 * self.steps

    def update(self) -> Vector:

        dn = self.game.snake.p.y
        de = self.game.grid.x - self.game.snake.p.x
        ds = self.game.grid.y - self.game.snake.p.y
        dw = self.game.snake.p.x

        # normalized

        # dn = dn / self.game.grid.y
        # de = de / self.game.grid.x
        # ds = ds / self.game.grid.y
        # dw = dw / self.game.grid.x

        dfx = self.game.snake.p.x - self.game.food.p.x
        dfy = self.game.snake.p.y - self.game.food.p.y

        # normalized

        # dfx = dfx / self.game.grid.x
        # dfy = dfy / self.game.grid.y

        df = np.sqrt(
            (self.game.snake.p.x - self.game.food.p.x) ** 2
            + (self.game.snake.p.y - self.game.food.p.y) ** 2
        )

        # normalized

        # df = df / np.sqrt(self.game.grid.x**2 + self.game.grid.y**2)

        s = self.game.snake.score

        obs = (dn, de, ds, dw, dfx, dfy, df, s)
        # print(obs)

        action = self.model.action(obs)
        next_move = self.action_space[action]

        if self.display:
            self.screen.fill("black")
            for i, p in enumerate(self.game.snake.body):
                pygame.draw.rect(
                    self.screen,
                    (0, max(128, 255 - i * 12), 0),
                    self.block(p),
                )
            pygame.draw.rect(self.screen, self.color_food, self.block(self.game.food.p))
            pygame.display.flip()
            self.clock.tick(10)

        self.steps += 1
        self.model.set_fitness(self.fitness)
        return next_move

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
