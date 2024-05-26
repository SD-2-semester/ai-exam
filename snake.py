import random
from collections import deque
from typing import Protocol
import pygame
from vector import Vector


class SnakeGame:
    def __init__(self, xsize: int = 30, ysize: int = 30, scale: int = 15):
        self.grid = Vector(xsize, ysize)
        self.scale = scale
        self.snake = Snake(game=self)
        self.food = Food(game=self)
        self.running = True

    def run(self):

        while self.running:
            next_move = self.controller.update()

            if self.controller.steps >= 1000:
                message = "Number of moves exceeded."
                self.snake.score = -1000 if self.snake.score < 1 else self.snake.score
                self.running = False
            if next_move:
                if self.snake.v != next_move:
                    print("added score")
                    self.snake.score += 1
                self.snake.v = next_move
                self.snake.move()
            if not self.snake.p.within(self.grid):
                self.snake.remove_score()
                self.running = False
                message = "Game over! You crashed into the wall!"

            if self.snake.cross_own_tail:
                self.snake.remove_score()
                self.running = False
                message = "Game over! You hit your own tail!"

            if self.snake.p == self.food.p:
                self.snake.add_score()
                self.food = Food(game=self)
        print(f"{message} ... Score: {self.snake.score}")


class Food:
    def __init__(self, game: SnakeGame):
        self.game = game
        self.p = Vector.random_within(self.game.grid)


class Snake:
    def __init__(self, *, game: SnakeGame):
        self.game = game
        self.score = 0
        self.v = Vector(0, 0)
        self.body = deque()
        self.body.append(Vector.random_within(self.game.grid))
        tail = self.body[0]
        self.body.append(tail)

    def move(self):
        self.p = self.p + self.v

    @property
    def cross_own_tail(self):
        try:
            self.body.index(self.p, 1)
            return True
        except ValueError:
            return False

    @property
    def p(self):
        return self.body[0]

    @p.setter
    def p(self, value):
        self.body.appendleft(value)
        self.body.pop()

    def add_score(self):
        self.score += 1000
        tail = self.body.pop()
        self.body.append(tail)
        self.body.append(tail)

    def remove_score(self):
        self.score -= 100

    def debug(self):
        print("===")
        for i in self.body:
            print(str(i))
