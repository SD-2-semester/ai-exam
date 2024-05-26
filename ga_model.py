from math import tan
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
        for i, dim in enumerate(dims):
            if i < len(dims) - 1:
                self.DNA.append(np.random.rand(dim, dims[i + 1]))

    def update(self, obs):
        x = obs
        # print("before", x)
        for i, layer in enumerate(self.DNA):
            if not i == 0:
                x = tanh(x)
            # print(layer)
            x = x @ layer
        # print("after", x)
        soft_max = softmax(x)
        return soft_max

    def action(self, obs):
        action = self.update(obs)
        return action.argmax()
        # return random.randint(0, 3)

    def mutate(self, mutation_rate, intensity) -> None:
        if random.random() < mutation_rate:
            for i in range(len(self.DNA)):
                mutant_dna_layer = np.empty(self.DNA[i].shape)
                for j in range(len(self.DNA[i])):
                    self_dna_layer = np.array(self.DNA[i][j])
                    rand_dna_layer = np.random.rand(*self_dna_layer.shape)
                    rand_mask = np.random.rand(*self_dna_layer.shape) > intensity
                    new_dna_layer = np.where(rand_mask, self_dna_layer, rand_dna_layer)
                    mutant_dna_layer[j] = new_dna_layer
                self.DNA[i] = mutant_dna_layer
            print("mutation done.")

    def __add__(self, other: "SimpleModel"):
        baby_snake_DNA = []

        for i in range(len(self.DNA)):
            baby_dna_layer = np.empty(self.DNA[i].shape)
            for j in range(len(self.DNA[i])):
                self_dna_layer = np.array(self.DNA[i][j])
                other_dna_layer = np.array(other.DNA[i][j])
                rand_mask = np.random.rand(*self_dna_layer.shape) > 0.5
                baby_dna_gene = np.where(rand_mask, self_dna_layer, other_dna_layer)
                baby_dna_layer[j] = baby_dna_gene
            baby_snake_DNA.append(baby_dna_layer)
        baby = type(self)(dims=self.dims)
        baby.DNA = baby_snake_DNA
        return baby

    def get_shapes(self):
        # Returns a list of shapes of the arrays in self.DNA
        return [arr.shape for arr in self.DNA]

    def print_shapes(self):
        # Prints the shapes of the arrays in self.DNA
        for arr in self.DNA:
            print(arr.shape)
