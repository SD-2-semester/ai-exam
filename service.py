import matplotlib.pyplot as plt


class EvolutionTracker:
    def __init__(self):

        self.generation_number = []
        self.score_list = []
        self.fitness_list = []

        plt.ion()  # interactive mode
        self.fig, self.ax = plt.subplots()

    def add_data(self, generation_no: int, score: int, fitness: float):
        """Append new data to the lists and update the plot."""
        self.generation_number.append(generation_no)
        self.score_list.append(score)
        self.fitness_list.append(fitness)

        # clear the previous plot
        self.ax.clear()

        # updated data
        self.ax.plot(self.generation_number, self.score_list, label="Score")
        self.ax.plot(self.generation_number, self.fitness_list, label="Fitness")
        self.ax.set_xlabel("Generation Number")
        self.ax.set_ylabel("Values")
        self.ax.legend()

        # redraw the plot and pause to update the display
        plt.draw()
        plt.pause(0.1)

    def finalize(self):
        """Keep the window open after updates are complete."""
        plt.ioff()
        plt.show()

