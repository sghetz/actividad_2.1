import subject_schedule

generate_subject_schedule = subject_schedule.generate_subject_schedule
# Definición de la estructura de datos para representar un cromosoma
class Chromosome:
    def __init__(self, schedule):
        self.schedule = schedule

    def __repr__(self):
        return str(self.schedule)

# Generación de la población inicial
def generate_initial_population(subjects, population_size):
    population = []
    for _ in range(population_size):
        schedule = {subject: generate_subject_schedule(subject) for subject in subjects}
        chromosome = Chromosome(schedule)
        population.append(chromosome)
    return population

# Ejemplo de materias
subjects = ["TC1030", "TC2006B"]  # Ejemplo de materias

# Generación de población inicial
population_size = 5
population = generate_initial_population(subjects, population_size)

# Mostrar la población inicial
for i, chromosome in enumerate(population):
    print(f"Chromosome {i}: {chromosome}")
