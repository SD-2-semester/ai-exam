import gym
from ga_model import SimpleModel
from population import Population
from service import load_model, save_model, EvolutionTracker


def create_environment(render_mode=None):
    return gym.make("LunarLander-v2", render_mode=render_mode)


# Start with no rendering for faster execution
env = create_environment()

if __name__ == "__main__":
    tracker = EvolutionTracker()
    filename = "./models/best_model"
    pop_size = 100
    generations = 50
    population = Population(size=pop_size, dims=(8, 32, 32, 32, 4))
    verbose = True
    high_score = 0
    best_model = None
    load_best_model = False

    for generation in range(generations):
        if generation == generations - 2:
            env.close()  # Close the current environment without rendering
            env = create_environment(render_mode="human")
        for model in population:
            # if load_best_model:
            #     model = load_model(filename=filename)
            observation, info = env.reset(seed=42)
            score = 0

            for _ in range(5000):
                action = model.action(obs=observation)  # Get action from model
                observation, reward, terminated, truncated, info = env.step(action)
                score += reward

                if terminated or truncated:
                    break

            model.fitness = score
            if verbose and score > high_score:
                high_score = score
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

    # Close the environment only once, when it is no longer needed.
    env.close()
    print(f"Best Model Fitness: {population.best_fit().fitness}")
    save_model(model=best_model, filename=filename)
    tracker.finalize()
