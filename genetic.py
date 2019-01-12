import pathing as pt
from random import random, choice
import numpy as np
import copy


def init_population(population, size, source_station, destination_station):
    for i in range(size):
        population.append(pt.path_finding(source_station, destination_station))


def crossover(ind1, ind2):
    path1 = ind1.stations[1:-1]
    path2 = ind2.stations[1:-1]

    coincidences = []

    for station in path1:
        if station in path2:
            coincidences.append(station)

    if not coincidences:
        return [False, False]

    station = choice(coincidences)
    index1 = path1.index(station)
    index2 = path2.index(station)

    stations_1_1 = ind1.stations[:index1+1]
    stations_1_2 = ind1.stations[index1+1:]
    stations_2_1 = ind2.stations[:index2 + 1]
    stations_2_2 = ind2.stations[index2 + 1:]

    time_1_1 = ind1.time[:index1]
    time_1_2 = ind1.time[index1:]
    time_2_1 = ind2.time[:index2]
    time_2_2 = ind2.time[index2:]

    lines_1_1 = ind1.lines[:index1]
    lines_1_2 = ind1.lines[index1:]
    lines_2_1 = ind2.lines[:index2]
    lines_2_2 = ind2.lines[index2:]

    stations_1_1.extend(stations_2_2)
    time_1_1.extend(time_2_2)
    lines_1_1.extend(lines_2_2)

    stations_2_1.extend(stations_1_2)
    time_2_1.extend(time_1_2)
    lines_2_1.extend(lines_1_2)

    new_individual_1 = pt.Individual(stations_1_1, time_1_1, lines_1_1)
    new_individual_2 = pt.Individual(stations_2_1, time_2_1, lines_2_1)

    return [new_individual_1, new_individual_2]


def mutation(individual):
    source_station = individual.stations[0]
    mutate = round(random() * (len(individual.stations) - 3) + 1)
    destination_station = individual.stations[mutate]

    stations = individual.stations[mutate + 1:]
    time = individual.time[mutate:]
    lines = individual.lines[mutate:]

    new_individual = pt.path_finding(source_station, destination_station)

    new_stations = new_individual.stations
    new_time = new_individual.time
    new_lines = new_individual.lines

    new_stations.extend(stations)
    new_time.extend(time)
    new_lines.extend(lines)

    new_individual.stations = new_stations
    new_individual.time = new_time
    new_individual.lines = new_lines

    return new_individual


def get_fitness(individual, initial_time):
    individual.transfer_time = pt.get_transfer_time(individual, initial_time)
    return 100 / (2 * (sum(individual.time) + individual.transfer_time) + 10 * pt.get_line_changes(individual.lines))


def genetic(source_station, destination_station, initial_time, population_size, elitism, mutation_prob, iterations=50):

    if elitism % 2 == 1 or population_size % 2 == 1:
        print("Parameters elitism and size must be even")
        return None

    if elitism > population_size:
        print("Parameter elitism must be less than the population size")
        return None

    if elitism < 0 or population_size < 0:
        print("Parameters elitism and population_size must be greater than zero")
        return None

    population = []
    init_population(population, population_size, source_station, destination_station)

    for individual in population:
        individual.fitness = get_fitness(individual, initial_time)

    for _ in range(iterations):
        population.sort(key=lambda x: x.fitness, reverse=True)

        next_population = []
        next_population.extend(population[:elitism])

        sum_fitness = sum([individual.fitness for individual in population])
        prob = []

        for value in [individual.fitness for individual in population]:
            prob.append(value/sum_fitness)

        for i in range(int((population_size - elitism) / 2)):
            couple = np.random.choice([i for i in range(population_size)], 2, p=prob, replace=False)
            if len(population[couple[0]].stations) < 3 or len(population[couple[1]].stations) < 3:
                [ind1, ind2] = [population[couple[0]], population[couple[1]]]
            else:
                [ind1, ind2] = crossover(population[couple[0]], population[couple[1]])
            next_population.append(ind1)
            next_population.append(ind2)

        for i, individual in enumerate(next_population):
            if random() < mutation_prob:
                next_population[i] = mutation(individual)

        for individual in next_population:
            if individual.fitness == 0:
                individual.fitness = get_fitness(individual, initial_time)

        population = copy.deepcopy(next_population)

    population.sort(key=lambda x: x.fitness, reverse=True)

    res = []

    for ind in population:
        if ind not in res:
            res.append(ind)

    return res[:4]

    # return population[:4]


departure_hour = pt.Hour(16, 30)
individuals = genetic("Sao Judas", "Belém", departure_hour, 300, 40, 0.1)

for ind in individuals:
    arrival_hour = departure_hour + sum(ind.time) + ind.transfer_time
    h = ""
    m = ""
    if arrival_hour.hour < 10:
        h = "0"
    if arrival_hour.minute < 10:
        m = "0"
    h += str(arrival_hour.hour)
    m += str(arrival_hour.minute)
    print("Route: {}\nTravel time: {}\nTransfer time: {}\nLines traveled: {}\nArrival time: {}:{}\n".
          format(ind.stations, sum(ind.time), ind.transfer_time, ind.lines, h, m))
