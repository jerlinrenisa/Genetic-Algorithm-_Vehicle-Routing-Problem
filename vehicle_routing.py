# -*- coding: utf-8 -*-
"""Vehicle Routing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MPAU8SRtfYgp_UXwpbzQNnLJka44XSmx
"""

#TASK 1 - Install matplotlib and deap
!pip install matplotlib deap

# Import all necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import random

# TODO: Task 2 - Define the number of locations and vehicles

num_locations = 10 # Define the number of locations (eg 10)

locations =[(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_locations)]  # Create a list of tuples representing location coordinates -
            # try to use a random number generator
            # (x, y) could be between 0 and 100

depot = (50, 50)# Define the coordinates for the depot

num_vehicles = 3 # Define the number of vehicles - (eg 3)

# TASK 3 - Genetic Algorithm Setup
       # - Figure out how to represent an individual OR encode an individual

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

#TASK 4 - Starting with the toolbox and tools

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(num_locations), num_locations)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Evaluation function
def evalVRP(individual):
    total_distance = 0
    # Split the list of locations among vehicles, ensuring each starts and ends at the depot
    for i in range(num_vehicles):
        vehicle_route = [depot] + [locations[individual[j]] for j in range(i, len(individual), num_vehicles)] + [depot]
        vehicle_distance = sum(
            np.linalg.norm(np.array(vehicle_route[k + 1]) - np.array(vehicle_route[k]))
            for k in range(len(vehicle_route) - 1)
        )
        total_distance += vehicle_distance
    return total_distance,  # Return a tuple

toolbox.register("evaluate", evalVRP)

# Task 7: Configure the genetic operators
toolbox.register("mate", tools.cxPartialyMatched)# Use Partially Matched Crossover (PMX)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.5)# Use Shuffle Indexes Mutation
toolbox.register("select", tools.selTournament, tournsize=3)# Use Tournament Selection

#TASK 8 - Plotting Function
def plot_routes(individual, title="Routes"):
    plt.figure()
    # Plot locations as blue dots and the depot as a red square
    for (x, y) in locations:
        plt.plot(x, y, 'bo')
    plt.plot(depot[0], depot[1], 'rs')

    # Draw routes for each vehicle
    for i in range(num_vehicles):
        vehicle_route = [depot] + [locations[individual[j]] for j in range(i, len(individual), num_vehicles)] + [depot]
        plt.plot(*zip(*vehicle_route), '-')

    plt.title(title)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()

# Running the Genetic Algorithm
def main():
    random.seed(42)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)

    algorithms.eaSimple(pop, toolbox, 0.7, 0.2, 30, stats=stats, halloffame=hof)
    return pop, stats, hof

if __name__ == "__main__":
    population, stats, hall_of_fame = main()
    best_individual = hall_of_fame[0]
    print("Best Individual:", best_individual)
    print("Best Fitness:", evalVRP(best_individual))
    plot_routes(best_individual)

