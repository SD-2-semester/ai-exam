import random


class Vector:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def within(self, scope: "Vector") -> "Vector":
        return self.x <= scope.x and self.x >= 0 and self.y <= scope.y and self.y >= 0

    def __eq__(self, other: "Vector") -> bool:
        return self.x == other.x and self.y == other.y

    @classmethod
    def random_within(cls, scope: "Vector") -> "Vector":
        return Vector(
            random.randint(0, scope.x - 1.0), random.randint(0, scope.y - 1.0)
        )

    def length(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self) -> "Vector":
        length = self.length()
        return Vector(self.x / length, self.y / length)
