from ga_model import SimpleModel
from typing import Type

import random


class Population:
    def __init__(
        self,
        target: Type[SimpleModel],
        size: int,
        dims: tuple[int, ...] = (8, 7, 16, 15, 3),
    ):
        self.mutation_rate = 0.02
        self.population = [target(dims=dims) for _ in range(size)]

    def __iter__(self):
        return iter(self.population)

    def __getitem__(self, index):
        return self.population[index]

    def __setitem__(self, index, value):
        self.population[index] = value

    def __len__(self):
        return len(self.population)

    def mutate(self):
        for model in self.population:
            model.mutate(self.mutation_rate)

    def selection(self):
        self.population = sorted(
            self.population, key=lambda x: x.fitness(), reverse=True
        )
        self.population = self.population[len(self.population) // 2 :]
        while len(self.population) < 100:
            parents = random.sample(self.population, 2)
            baby = parents[0] + parents[1]
            self.population.append(baby)

    def best_fit(self) -> float:
        best = sorted(self.population, key=lambda x: x.fitness(), reverse=True)[0]
        return best.fitness()


#
# def selection(self, top_half: int):
#    result_generation = [(model.fitness, model) for model in self.population]
#    result_generation.sort(key=lambda x: x[0], reverse=True)
#    top_half_population = [model for _, model in result_generation[: top_half // 2]]
#    return top_half_population
