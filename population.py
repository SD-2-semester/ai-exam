import random
from ga_model import SimpleModel
from typing import Iterator


class Population:

    def __init__(
        self,
        size: int,
        dims: tuple[int, ...] = (12, 64, 32, 4),
    ):
        self.size = size
        self.population = [SimpleModel(dims=dims) for _ in range(size)]

        self.mutation_rate = 0.02
        self.intensity = 0.1

    def __iter__(self) -> Iterator[SimpleModel]:
        return iter(self.population)

    def __getitem__(self, index: int) -> SimpleModel:
        return self.population[index]

    def __len__(self) -> int:
        return len(self.population)

    def __setitem__(self, index: int, value: SimpleModel) -> None:
        self.population[index] = value

    def mutate(self) -> None:
        for model in self.population:
            model.mutate(self.mutation_rate, self.intensity)

    def selection(self) -> None:
        # sort and select the top half
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        self.population = self.population[: self.size // 2]

        # crossover
        while len(self.population) < self.size:
            parents = self.population[:2]
            baby = parents[0] + parents[1]
            self.population.append(baby)

    def best_fit(self) -> SimpleModel:
        return max(self.population, key=lambda x: x.fitness)
