#!/usr/bin/env python


from snake import SnakeGame
from ga_controller import GAController
from ga_model import SimpleModel


if __name__ == "__main__":

    population = [SimpleModel(dims=(7, 4, 3)) for _ in range(1000)]
    test = []
    for i in range(2):
        game = SnakeGame()
        model = SimpleModel(dims=(7, 4, 3))

        #model.mutate(0.2)
        controller = GAController(game, model, display=True)
        game.run()


        test.append((controller.fitness, model))

        del controller
    print(test)

    print(test[0][1] + test[0][1])