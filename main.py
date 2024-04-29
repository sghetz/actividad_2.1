import random
import udf_data_format
import professor_data_format

professors = professor_data_format.professors
UDF = udf_data_format.UDF

schedules = {
    "Monday": ["07-09", "09-11", "11-13", "15-17", "17-19", "19-21"],
    "Tuesday": ["07-09", "09-11", "11-13", "15-17", "17-19", "19-21"],
    "Thursday": ["07-09", "09-11", "11-13", "15-17", "17-19", "19-21"],
    "Friday": ["07-09", "09-11", "11-13", "15-17", "17-19", "19-21"]
}

# Constraints
max_hours_per_day = 8
max_hours_per_week = 20

# Define the individual (chromosome) representation
def create_individual():
    return {uf: (random.choice(list(professors.keys())), random.choice(list(schedules.keys()))) for uf in UDF}

# Define the population
def create_population(population_size):
    return [create_individual() for _ in range(population_size)]

# Define the fitness function (cost function)
def fitness(individual):
    professor_hours_per_day = {prof: 0 for prof in professors}
    professor_hours_per_week = {prof: 0 for prof in professors}
    for uf, (professor, day) in individual.items():
        professor_hours_per_day[professor] += 1
        professor_hours_per_week[professor] += 1
    penalty = sum(max(0, hours - max_hours_per_day) for hours in professor_hours_per_day.values()) + \
              sum(max(0, hours - max_hours_per_week) for hours in professor_hours_per_week.values())
    return penalty

# Define the selection method (tournament selection)
def selection(population, tournament_size):
    selected_parents = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        selected_parents.append(min(tournament, key=fitness))
    return selected_parents

# Define the crossover method (single-point crossover)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(UDF) - 1)
    child = {}
    for idx, uf in enumerate(UDF):
        if idx < crossover_point:
            child[uf] = parent1[uf]
        else:
            child[uf] = parent2[uf]
    return child

# Define the mutation method (random mutation)
def mutation(individual, mutation_rate):
    mutated_individual = individual.copy()
    for uf in UDF:
        if random.random() < mutation_rate:
            mutated_individual[uf] = (random.choice(list(professors.keys())), random.choice(list(schedules.keys())))
    return mutated_individual

# Define the genetic algorithm
def genetic_algorithm(population_size, num_generations, tournament_size, mutation_rate):
    population = create_population(population_size)
    for _ in range(num_generations):
        parents = selection(population, tournament_size)
        next_generation = []
        for _ in range(population_size):
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            next_generation.append(child)
        population = next_generation
    best_individual = min(population, key=fitness)
    return best_individual

# Example usage
best_solution = genetic_algorithm(population_size=100, num_generations=100, tournament_size=5, mutation_rate=0.1)

# Print best solution found
print("Best solution found:")
for uf, (professor, day) in best_solution.items():
    print(f"UF: {uf} | Professor: {professor} | Day: {day}")
