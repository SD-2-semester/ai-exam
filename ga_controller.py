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
        snake_body = self.game.snake.body
        position_food = self.game.food.p

        # Calculate snake direction
        head_pos = self.game.snake.body[0]
        next_pos = self.game.snake.body[1]
        direction_x = (
            head_pos.x - next_pos.x
        )  # Positive if moving right, negative if left
        direction_y = head_pos.y - next_pos.y  # Positive if moving down, negative if up

        normalized_direction_x = 1 if direction_x > 0 else 0
        normalized_direction_y = 1 if direction_y > 0 else 0

        food_direction_x = position_food.x - head_pos.x
        food_position_y = position_food.y - head_pos.y
        # Is the food to the left of the snake?

        # print(self.update_observations(self.game.snake, self.game.food, self.game.grid))

        obs_dict = self.update_observations(
            self.game.snake, self.game.food, self.game.grid
        )
        obs = (
            direction_x,
            direction_y,
            food_direction_x,
            food_position_y,
            obs_dict["danger_up"],
            obs_dict["danger_down"],
            obs_dict["danger_left"],
            obs_dict["danger_right"],
            obs_dict["food_distance"],
            obs_dict["food_angle"],
            obs_dict["distance_to_left_wall"],
            obs_dict["distance_to_right_wall"],
            obs_dict["distance_to_top_wall"],
            obs_dict["distance_to_bottom_wall"],
        )
        # print(obs)

        action = self.model.action(obs)
        next_move = self.action_space[action]
        try:
            if self.display:
                self.screen.fill("black")
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
                self.clock.tick(24)

            self.steps += 1
        except Exception as e:
            print(e)
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

    def calculate_relative_food_position(self, snake_head, food_position):
        vector_to_food = np.array(
            [food_position.x - snake_head.x, food_position.y - snake_head.y]
        )
        distance = np.linalg.norm(vector_to_food)
        angle = np.arctan2(vector_to_food[1], vector_to_food[0])
        return (
            distance / np.sqrt(self.game.grid.x**2 + self.game.grid.y**2),
            angle / np.pi,
        )  # Normalized

    def check_directional_danger(self, snake, direction, grid_size):
        head_x, head_y = snake.body[0].x, snake.body[0].y
        next_position = {
            "up": (head_x, head_y - 1),
            "down": (head_x, head_y + 1),
            "left": (head_x - 1, head_y),
            "right": (head_x + 1, head_y),
        }
        next_x, next_y = next_position[direction]

        # Check wall collisions
        if next_x < 0 or next_x >= grid_size.x or next_y < 0 or next_y >= grid_size.y:
            return 1  # Danger

        # Check self collisions
        if (next_x, next_y) in [
            (s.x, s.y) for s in list(snake.body)[1:]
        ]:  # Exclude the head in comparison
            return 1  # Danger

        return 0  # No danger

    def calculate_wall_distance(self, snake_head, grid_size):
        distances = {
            "distance_to_left_wall": snake_head.x,
            "distance_to_right_wall": grid_size.x - snake_head.x - 1,
            "distance_to_top_wall": snake_head.y,
            "distance_to_bottom_wall": grid_size.y - snake_head.y - 1,
        }
        # Normalize distances
        for key in distances:
            distances[key] /= max(grid_size.x, grid_size.y)
        return distances

    def update_observations(self, snake, food, grid_size):
        obs = {}
        directions = ["up", "down", "left", "right"]

        # Danger checks
        for direction in directions:
            obs[f"danger_{direction}"] = self.check_directional_danger(
                snake, direction, grid_size
            )

        # Food relative position
        distance, angle = self.calculate_relative_food_position(snake.body[0], food.p)
        obs["food_distance"] = distance
        obs["food_angle"] = angle

        # Wall proximity
        obs.update(self.calculate_wall_distance(snake.body[0], grid_size))

        return obs
