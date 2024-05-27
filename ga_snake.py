from snake import SnakeGame
from ga_controller import GAController
from ga_model import SimpleModel

if __name__ == "__main__":

    generations = 202
    population_size = 50
    snake_population = [
        SimpleModel(dims=(12, 64, 32, 4)) for _ in range(population_size)
    ]
    high_score = 0
    generation_highscore = 0
    snake_highscore = SimpleModel(dims=(9, 2, 3))
    display = False

    for generation in range(generations):
        snake_number = 0
        result_generation = []
        for snake in snake_population:
            print(
                f"**** Current Generation: {generation}, high_score so far: {high_score}, by generation {generation_highscore}"
            )
            snake_number += 1
            # print("snake number: ", snake_number)
            game = SnakeGame()

            if generation > 200:
                display = True

            controller = GAController(game, snake, display=display)

            game.run()
            # print(f"snake fitnes:{controller.fitness} and score: {controller.score}")
            if controller.game.snake.score > high_score:
                high_score = controller.score
                generation_highscore = generation
                snake_highscore = snake
            # print(snake_number, "Snake dna: ", snake.DNA)
            # print(snake_number, "Snake dna: ", snake.get_shapes())

            result_generation.append((controller.fitness, snake))

        # Sort results by fitness in descending order
        result_generation.sort(key=lambda x: x[0], reverse=True)

        # Select the top 50% of the results
        top_half_population = [
            model for _, model in result_generation[: population_size // 2]
        ]
        # Generate new population through crossover and mutation
        new_population = []
        for i in range(0, len(top_half_population), 2):
            parent1 = top_half_population[i]
            parent2 = (
                top_half_population[i + 1]
                if i + 1 < len(top_half_population)
                else top_half_population[0]
            )
            child1 = parent1 + parent2
            child2 = parent2 + parent1
            child1.mutate(0.2, 0.3)
            child2.mutate(0.2, 0.3)
            new_population.extend([child1, child2])

        # Ensure the new population is the same size as the original
        # print(len(new_population))
        if len(new_population) < population_size:
            new_population.extend(
                top_half_population[: population_size - len(new_population)]
            )

        # print("Top 10: ", result_generation[:10])
        snake_population = new_population
        if result_generation:
            print(f"Generation {generation} best fitness: {result_generation[0][0]}")
        print(f"Generation {generation}")
        # print(" ")
    print("best_snake_dna:", snake_highscore.DNA)
