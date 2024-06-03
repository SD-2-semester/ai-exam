import matplotlib.pyplot as plt
import pickle


class EvolutionTracker:
    def __init__(self):
        self.generation_number = []
        self.score_list = []
        self.fitness_list = []

        plt.ion()  # interactive mode
        self.fig, self.ax = plt.subplots()
        self.ax2 = self.ax.twinx()  # Create a twin of the original axis for fitness

    def add_data(self, generation_no: int, score: int, fitness: float):
        """Append new data to the lists and update the plot."""
        self.generation_number.append(generation_no)
        self.score_list.append(score)
        self.fitness_list.append(fitness)

        # Clear the previous plot
        self.ax.clear()
        self.ax2.clear()

        # Update data for score on the original axis
        self.ax.plot(self.generation_number, self.score_list, "b-", label="High Score")
        self.ax.set_xlabel("Generation Number")

        # Update data for fitness on the twin axis
        self.ax2.plot(self.generation_number, self.fitness_list, "g-", label="Fitness")

        # Add legends
        self.ax.legend(loc="upper left")
        self.ax2.legend(loc="upper right")

        # Redraw the plot and pause to update the display
        plt.draw()
        plt.pause(0.1)

    def finalize(self):
        """Keep the window open after updates are complete."""
        plt.ioff()
        plt.show()


def save_model(model, filename):
    """Save the given model to a file."""
    with open(filename, "wb") as f:
        pickle.dump(model, f)


def load_model(filename):
    """Load a model from a file."""
    with open(filename, "rb") as f:
        return pickle.load(f)
