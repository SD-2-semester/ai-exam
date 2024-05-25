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
        score = self.score * 100 if self.score >= 1 else 0
        return score / (np.log(self.steps + 1)) - 0.01 * self.steps

    def update(self) -> Vector:

        # Positions
        position_snake = self.game.snake.body[0]
        position_food = self.game.food.p

        # Calculate snake direction
        if len(self.game.snake.body) > 1:
            head_pos = self.game.snake.body[0]
            next_pos = self.game.snake.body[1]
            direction_x = (
                head_pos.x - next_pos.x
            )  # Positive if moving right, negative if left
            direction_y = (
                head_pos.y - next_pos.y
            )  # Positive if moving down, negative if up
        else:
            direction_x, direction_y = 0, 0  # No movement if snake has only one segment

        # Distance to wall
        distance_north_snake_wall = self.game.snake.p.y
        distance_east_snake_wall = self.game.grid.x - self.game.snake.p.x
        distance_south_snake_wall = self.game.grid.y - self.game.snake.p.y
        distance_west_snake_wall = self.game.snake.p.x

        distance_snake_food_x = self.game.snake.p.x - self.game.food.p.x
        distance_snake_food_y = self.game.snake.p.y - self.game.food.p.y

        # Calculate Euclidean distance to the food
        distance_euclidean_food = np.sqrt(
            (self.game.snake.p.x - self.game.food.p.x) ** 2
            + (self.game.snake.p.y - self.game.food.p.y) ** 2
        )

        # Score
        score = self.game.snake.score

        # Normalize position of snake and food
        normalized_position_snake_x = self.normalize(position_snake.x, self.game.grid.x)
        normalized_position_snake_y = self.normalize(position_snake.y, self.game.grid.y)
        normalized_position_food_x = self.normalize(position_food.x, self.game.grid.x)
        normalized_position_food_y = self.normalize(position_food.y, self.game.grid.y)

        # Normalize distances to walls
        normalized_distance_north_snake_wall = self.normalize(
            distance_north_snake_wall, self.game.grid.y
        )
        normalized_distance_south_snake_wall = self.normalize(
            distance_south_snake_wall, self.game.grid.y
        )
        normalized_distance_east_snake_wall = self.normalize(
            distance_east_snake_wall, self.game.grid.x
        )
        normalized_distance_west_snake_wall = self.normalize(
            distance_west_snake_wall, self.game.grid.x
        )

        # Normalize distances between snake and food
        normalized_distance_snake_food_x = self.normalize(
            abs(distance_snake_food_x), self.game.grid.x
        )
        normalized_distance_snake_food_y = self.normalize(
            abs(distance_snake_food_y), self.game.grid.y
        )

        # Normalize Euclidean distance
        max_distance = np.sqrt(self.game.grid.x**2 + self.game.grid.y**2)
        normalized_distance_euclidean_food = self.normalize(
            distance_euclidean_food, max_distance
        )

        # Assuming direction can be -1, 0, or 1, it's already normalized to a degree, but let's scale it to [0, 1]
        normalized_direction_x = (direction_x + 1) / 2
        normalized_direction_y = (direction_y + 1) / 2

        # Normalize score if there's a known max score, otherwise, it can be scaled by some large number or average score expected
        max_score = 100  # Example max score, adjust based on game specifics
        normalized_score = self.normalize(score, max_score)

        # Recreate the observation tuple with normalized values
        obs = (
            normalized_position_snake_x,
            normalized_position_snake_y,
            normalized_direction_x,
            normalized_direction_y,
            normalized_position_food_x,
            normalized_position_food_y,
            normalized_distance_north_snake_wall,
            normalized_distance_south_snake_wall,
            normalized_distance_east_snake_wall,
            normalized_distance_west_snake_wall,
            normalized_distance_snake_food_x,
            normalized_distance_snake_food_y,
            normalized_distance_euclidean_food,
            normalized_score,
        )

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

    def normalize(self, value, max_value):
        return value / max_value
