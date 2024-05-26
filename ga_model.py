import random
import numpy as np


def softmax(z):
    return np.exp(z) / np.sum(np.exp(z))


def tanh(z):
    return np.tanh(z)


def relu(z):
    return np.maximum(0, z)


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)


class SimpleModel:
    def __init__(self, *, dims: tuple[int, ...]):
        self.dims = dims
        self.DNA = []
        self._fitness = 0
        for i, dim in enumerate(dims):
            if i < len(dims) - 1:
                self.DNA.append(
                    np.random.uniform(low=-1, high=1, size=(dim, dims[i + 1]))
                )

    def update(self, obs):
        x = obs
        for i, layer in enumerate(self.DNA):
            if not i == 0:
                x = tanh(x)
            x = x @ layer

        soft_max = softmax(x)
        return soft_max

    def action(self, obs):
        action = self.update(obs)
        return action.argmax()
        # return random.randint(0, 3)

    def mutate(self, mutation_rate) -> None:
        if random.random() < mutation_rate:
            random_layer = random.randint(0, len(self.DNA) - 1)
            row = random.randint(0, self.DNA[random_layer].shape[0] - 1)
            col = random.randint(0, self.DNA[random_layer].shape[1] - 1)
            self.DNA[random_layer][row][col] = random.uniform(-1, 1)

    def fitness(self):
        return self._fitness

    def set_fitness(self, fitness):
        self._fitness = fitness

    # @classmethod
    # def copulate(cls, parents: tuple["SimpleModel", "SimpleModel"]):
    #     baby_DNA = []
    #     for p1, p2 in zip(parents[0].DNA, parents[1].DNA):
    #         baby_layer = np.empty(p1.shape)
    #         for i in range(len(p1)):
    #             baby_gene = np.random.choice([p1[i], p2[i]])
    #             baby_layer[i] = baby_gene
    #         baby_DNA.append(baby_layer)
    #     baby = cls(dims=parents[0].dims)

    #     baby.DNA = baby_DNA
    #     return baby

    def __add__(self, other: "SimpleModel"):
        baby_snake_DNA = []

        for i in range(len(self.DNA)):
            baby_dna_layer = np.empty(self.DNA[i].shape)
            for k in range(len(self.DNA[i])):
                self_dna_layer = np.array(self.DNA[i][k])
                other_dna_layer = np.array(other.DNA[i][k])
                rand_mask = np.random.rand(*self_dna_layer.shape) > 0.5
                baby_dna_gene = np.where(rand_mask, self_dna_layer, other_dna_layer)
                baby_dna_layer[k] = baby_dna_gene
            baby_snake_DNA.append(baby_dna_layer)
        baby = type(self)(dims=self.dims)
        baby.DNA = baby_snake_DNA
        return baby

    def __lt__(self, other: "SimpleModel"):
        return self.fitness() < other.fitness()

    def __eq__(self, other: "SimpleModel") -> bool:
        return self.fitness() == other.fitness()

    def get_shapes(self):
        # Returns a list of shapes of the arrays in self.DNA
        return [arr.shape for arr in self.DNA]

    def print_shapes(self):
        # Prints the shapes of the arrays in self.DNA
        for arr in self.DNA:
            print(arr.shape)
