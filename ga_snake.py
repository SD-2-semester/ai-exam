from population import Population
from snake import SnakeGame
from ga_controller import GAController

if __name__ == "__main__":

    pop_size = 50
    generations = 200
    population = Population(size=pop_size)
    verbose = True
    late_display = True

    high_score = 0

    for generation in range(generations):
        for model in population:

            display = False
            if late_display and generation > generations - 10:
                display = True

            game = SnakeGame(verbose=verbose)
            controller = GAController(game, model, display=display)
            game.run()

            if verbose and controller.score > high_score:
                high_score = controller.score

            if verbose:
                print(f"Current Generation: {generation} - High Score: {high_score}")

        population.selection()
        population.mutate()

    print(f"Best Snake: {population.best_fit().fitness}")
