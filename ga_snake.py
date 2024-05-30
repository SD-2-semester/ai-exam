from matplotlib.mlab import GaussianKDE
from population import Population
from snake import SnakeGame
from ga_controller import GAController
from service import load_model, save_model, EvolutionTracker

if __name__ == "__main__":
    tracker = EvolutionTracker()
    filename = "./models/best_model"
    pop_size = 50
    generations = 200
    population = Population(size=pop_size)
    verbose = True
    late_display = True
    high_score = 0
    best_model = None

    load_best_model = False

    for generation in range(generations):
        for model in population:
            model = load_model(filename=filename) if load_best_model else model

            display = False
            if late_display and generation > generations - 1:
                display = True

            game = SnakeGame(verbose=verbose)
            controller = GAController(game, model, display=display)
            game.run()

            if verbose and controller.score > high_score:
                high_score = controller.score
                best_model = model

            if verbose:
                print(f"Current Generation: {generation} - High Score: {high_score}")
        tracker.add_data(
            generation_no=generation,
            score=high_score,
            fitness=population.best_fit().fitness,
        )

        population.selection()
        population.mutate()

    print(f"Best Snake: {population.best_fit().fitness}")
    save_model(model=best_model, filename=filename)
    tracker.finalize()
