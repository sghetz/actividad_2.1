import random
import json
import matplotlib.pyplot as plt

# Define the JSON data for subjects, professors, and modules
# These are simplified examples and may need to be adjusted based on the actual data format

udf_json_path = "json\\udf.json"

with open(udf_json_path, "r") as f:
    subjects_json = json.load(f)

professors_json = {
    "L03546291": {
        "name": "Pedro Hernandez Oregel",
        "email": "pedrohoregel@tec.mx",
        "area": "DB; data mining",
        "format": "physically",
        "schedule": {
            "monday": "07-11",
            "tuesday": "07-11",
            "wednesday": "07-11",
            "thursday": "07-11",
            "friday": "07-11"
        },
        "work": "null",
        "others": "null",
        "english": "null",
        "maxUdc": 14
    }
}

# Define defaults for the algorithm
days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
start_hours = [7, 9, 11, 13, 15, 17]

period_duration_mapping = {
    "PMT1": 5,
    "PMT2": 5,
    "PMT3": 5,
    "PMT4": 10,
    "PMT5": 10,
    "PMT6": 10
}

# Function to generate a subject schedule
def generate_subject_schedule(subject_data):
    total_hours = subject_data["hours"]
    start_hour = random.choice(start_hours)
    if "Professors" in subject_data:
        professor = random.choice(subject_data["Professors"])
        day = random.sample(days, 2)
        duration = int((total_hours / period_duration_mapping[subject_data["period"]]) / 2)
        return {"subject": subject_data["subject"], 
                "professor": professor, 
                "day": day, 
                "start_hour": start_hour, 
                "duration": duration, 
                "period": subject_data["period"], 
                "season": subject_data["season"]
                }
    elif "topic" in subject_data:
        topic_prof_map = []
        day = random.sample(days, 4)
        duration = int((total_hours / period_duration_mapping[subject_data["period"]]) / 4)
        for topic in subject_data["topic"]:
            topic_prof_map.append([topic["name"], random.choice(topic["professors"]), topic["hours"]])
        return {"subject": subject_data["subject"], 
                "topic/professors": topic_prof_map, 
                "day": day, "start_hour": start_hour, 
                "duration": duration, 
                "period": subject_data["period"], 
                "season": subject_data["season"]
                }
    else:
        professor = "Unknown"
        day = random.sample(days, 2)
        return {"subject": subject_data["subject"], 
                "professor": professor, 
                "day": day, 
                "start_hour": start_hour, 
                "duration": duration, 
                "period": subject_data["period"], 
                "season": subject_data["season"]
                }

# Function to generate the initial population
def generate_initial_population(subjects, population_size):
    population = []
    for _ in range(population_size):
        schedule = {subject_id: generate_subject_schedule(subjects[subject_id]) for subject_id in subjects}
        population.append(schedule)
    return population

def hard_constraints(schedule):
    # Verificar que no haya colisiones de horarios para el mismo profesor en diferentes materias o módulos
    professors_schedule = {}
    for subject_id in schedule:
        if "professor" in schedule[subject_id]:  # Materia regular
            professor = schedule[subject_id]["professor"]
            if professor in professors_schedule:
                if any(schedule_overlap(professors_schedule[professor], schedule[subject_id])):
                    return float('inf')  # Penalización por colisión de horarios
            professors_schedule[professor] = schedule[subject_id]
        elif "topic/professors" in schedule[subject_id]:  # Módulo
            topics = schedule[subject_id]["topic/professors"]
            for topic_info in topics:
                professors = topic_info[1]  # El profesor está en la posición 1 de la lista
                if not isinstance(professors, list):
                    professors = [professors]  # Convertir a lista si es un solo profesor
                for professor in professors:
                    if professor in professors_schedule:
                        if any(schedule_overlap(professors_schedule[professor], schedule[subject_id])):
                            return float('inf')  # Penalización por colisión de horarios
                    professors_schedule[professor] = schedule[subject_id]
    return 0


def soft_constraints(schedule):
    early_semester_penalty = sum(1 for subject_id in schedule if subjects_json[subject_id]["semester"] <= 2 and schedule[subject_id]["start_hour"] + schedule[subject_id]["duration"] > 19) * 5
    return early_semester_penalty

def schedule_overlap(schedule1, schedule2):
    day_overlap = schedule1["day"] == schedule2["day"]
    hour_overlap = schedule1["start_hour"] < schedule2["start_hour"] + schedule2["duration"] and schedule1["start_hour"] + schedule1["duration"] > schedule2["start_hour"]
    return [day_overlap and hour_overlap]  # Return a list containing the boolean result


# Función de evaluación
def evaluate_schedule(schedule):
    hard_score = hard_constraints(schedule)
    soft_score = soft_constraints(schedule)
    return hard_score, soft_score

# Funciones de selección, cruce y mutación
def select_parents(population, tournament_size=3):
    selected_parents = []
    while len(selected_parents) < 2:
        tournament = random.sample(population, tournament_size)
        best_chromosome = min(tournament, key=lambda x: sum(evaluate_schedule(x)))
        selected_parents.append(best_chromosome)
    return selected_parents

def crossover(parent1, parent2):
    child_schedule = {}
    for subject_id in parent1:
        if random.choice([True, False]):  # Se elige aleatoriamente un gen del padre 1 o padre 2
            child_schedule[subject_id] = parent1[subject_id]
        else:
            child_schedule[subject_id] = parent2[subject_id]
    return child_schedule


def mutate(schedule, mutation_rate=0.1):
    mutated_schedule = dict(schedule)  # Convertir a diccionario
    for subject_id in mutated_schedule:
        if random.random() < mutation_rate:
            mutated_schedule[subject_id] = generate_subject_schedule(subjects_json[subject_id])
    return mutated_schedule

# Algoritmo genético completo
def genetic_algorithm(subjects, population_size, generations):
    population = generate_initial_population(subjects, population_size)
    best_scores = []
    for _ in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population
        best_schedule = min(population, key=lambda x: sum(evaluate_schedule(x)))
        best_scores.append(sum(evaluate_schedule(best_schedule)))
    return best_schedule, best_scores


def plot_evolution(best_scores):
    plt.figure(figsize=(10, 6))
    plt.plot(best_scores, marker='o', color='b', linestyle='-')
    plt.title('Evolution of Best Score')
    plt.xlabel('Generation')
    plt.ylabel('Best Score')
    plt.grid(True)
    plt.show()

# Ejemplo de uso del algoritmo genético
if __name__ == "__main__":
    subjects = subjects_json
    best_solution, best_scores = genetic_algorithm(subjects, population_size=5, generations=1)
    print("Best schedule:")
    for subject_id in best_solution:
        print(f"{subject_id}: {best_solution[subject_id]}")
print(len(best_solution))

""" j = json.dumps(best_solution, indent=4, default=str)
with open('json\\time_table.json', 'w+') as f:
    print(j, file=f) """
