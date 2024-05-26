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
        self.biases = []
        for i, dim in enumerate(dims):
            if i < len(dims) - 1:
                self.DNA.append(
                    np.random.uniform(low=-1, high=1, size=(dim, dims[i + 1]))
                )
                self.biases.append(np.zeros(dims[i + 1]))  # Initialize biases to zero

    def update(self, obs):
        x = obs
        for i, (layer, bias) in enumerate(zip(self.DNA, self.biases)):
            x = x @ layer + bias  # Apply weights and add bias
            if (
                i < len(self.DNA) - 1
            ):  # Apply activation function to all but the last layer
                x = tanh(x)
        return softmax(x)  # Apply softmax to the output layer

    def action(self, obs):
        action = self.update(obs)
        return action.argmax()
        # return random.randint(0, 3)

    def mutate(self, mutation_rate, intensity) -> None:
        if random.random() < mutation_rate:
            for i in range(len(self.DNA)):
                # Mutate weights
                self_dna_layer = self.DNA[i]
                rand_dna_layer = np.random.rand(*self_dna_layer.shape)
                rand_mask = np.random.rand(*self_dna_layer.shape) > intensity
                self.DNA[i] = np.where(rand_mask, self_dna_layer, rand_dna_layer)
                # Mutate biases
                self_bias_layer = self.biases[i]
                rand_bias_layer = np.random.rand(*self_bias_layer.shape)
                rand_bias_mask = np.random.rand(*self_bias_layer.shape) > intensity
                self.biases[i] = np.where(
                    rand_bias_mask, self_bias_layer, rand_bias_layer
                )
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
