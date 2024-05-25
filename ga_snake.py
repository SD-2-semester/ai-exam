from snake import SnakeGame
from ga_controller import GAController
from ga_model import SimpleModel
from population import Population

if __name__ == "__main__":

    pop_size = 100
    generations = 100

    population = Population(target=SimpleModel, size=pop_size)

    for generation in range(generations):
        for model in population:
            game = SnakeGame()
            controller = GAController(game, model, display=False)
            game.run()
            # print(model)
            population.mutate()
            population.selection()
            bf = population.best_fit()

            # print(f"Score: {controller.score}, Fitness: {controller.fitness}")

        # population.mutate()
        # population.selection()
        # bf = population.best_fit()
#
# print(f"Generation: {generation}, Best Fitness: {bf},
#
# print(f"Generation: {generation}")

# generations = 100
# population_size = 100
# snake_population = [
#     SimpleModel(dims=(8, 7, 16, 15, 3)) for _ in range(population_size)
# ]
# high_score = 0
# genration_highscore = 0
# snake_highscore = SimpleModel(dims=(9, 2, 3))

# for generation in range(generations):
#     snake_number = 0
#     result_generation = []
#     for snake in snake_population:
#         print(
#             f"**** Current Generation: {generation}, high_score so far: {high_score}, by generation {genration_highscore}"
#         )
#         snake_number += 1
#         print("snake number: ", snake_number)
#         game = SnakeGame()

#         controller = GAController(game, snake, display=False)

#         game.run()
#         print(f"snake fitnes:{controller.fitness} and score: {controller.score}")
#         if controller.score > high_score:
#             high_score = controller.score
#             genration_highscore = generation
#             snake_highscore = snake
#         # print(snake_number, "Snake dna: ", snake.DNA)
#         # print(snake_number, "Snake dna: ", snake.get_shapes())

#         result_generation.append((controller.fitness, snake))

#     # Sort results by fitness in descending order
#     result_generation.sort(key=lambda x: x[0], reverse=True)

#     # Select the top 50% of the results
#     top_half_population = [
#         model for _, model in result_generation[: population_size // 2]
#     ]

#     # Generate new population through crossover and mutation
#     new_population = []
#     for i in range(0, len(top_half_population), 2):
#         parent1 = top_half_population[i]
#         parent2 = (
#             top_half_population[i + 1]
#             if i + 1 < len(top_half_population)
#             else top_half_population[0]
#         )
#         child1 = parent1 + parent2
#         child2 = parent2 + parent1
#         child1.mutate(0.2)
#         child2.mutate(0.2)
#         new_population.extend([child1, child2])

#     # Ensure the new population is the same size as the original
#     print(len(new_population))
#     if len(new_population) < population_size:
#         new_population.extend(
#             top_half_population[: population_size - len(new_population)]
#         )

#     print("Top 10: ", new_population[:10])
#     snake_population = new_population
#     print(f"Generation {generation} best fitness: {result_generation[0][0]}")
#     print(" ")
# print("best_snake_dna:", snake_highscore.DNA)
