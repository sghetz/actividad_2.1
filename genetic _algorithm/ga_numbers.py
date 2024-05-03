import random
import json

# Define the JSON data for subjects, professors, and modules
# These are simplified examples and may need to be adjusted based on the actual data format

udf_json_path = "json\\udf.json"

professor_json_path = "json\\professor_final.json"

with open(udf_json_path, "r") as u_json:
    subjects_json = json.load(u_json)

with open(professor_json_path, "r") as p_json:
    professors_json = json.load(p_json)

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

def find_matching_professor(partial_name, professors_json):
    matches = []
    for professor_name, professor_data in professors_json.items():
        if partial_name.lower() in professor_name.lower():
            matches.append((professor_name, professor_data.get("email"), professor_data.get("area")))
    return matches

def generate_subject_schedule(subject_data, professors_json, schedule):
    total_hours = subject_data["hours"]
    start_hour = random.choice(start_hours)  # Assuming start_hours is defined elsewhere
    if "Professors" in subject_data:
        professor = random.choice(subject_data["Professors"])
        matching_professor = find_matching_professor(professor, professors_json)
        if matching_professor:
            professor_schedule = matching_professor["schedule"]
            udc = subject_data.get("udc", 0)
            max_udc = matching_professor.get("maxUdc", float("inf"))
            assigned_udc = sum(subject_data["hours"] for sub_id, subject_data in schedule.items() if "professor" in subject_data and subject_data["professor"] == professor)
            if assigned_udc + total_hours > max_udc:
                return None  # Exceeds maxUdc
            day = random.sample(days, 2)
            duration = int((total_hours / period_duration_mapping[subject_data["period"]]) / 2)
            if duration > 2:
                duration = 2  # Limit the duration to 2 hours
            available_hours = [int(hour) for hour in professor_schedule[day[0]].split("-")]
            start_hour = max(start_hour, available_hours[0])
            start_hour = min(start_hour, available_hours[1] - duration)
            if start_hour % 2 == 0 and start_hour + 1 in range(available_hours[0], available_hours[1] + 1):
                start_hour += 1  # Move start hour to next odd hour
            return {"subject": subject_data["subject"],
                    "professor": professor,
                    "day": day,
                    "start_hour": start_hour,
                    "duration": duration,
                    "period": subject_data["period"],
                    "season": subject_data["season"]
                    }
        else:
            print(f"No se encontró un profesor que coincida con el nombre parcial '{professor}'.")
            return None
    elif "topic" in subject_data:
        topic_prof_map = []
        day = random.sample(days, 4)
        duration = int(total_hours / len(subject_data["topic"]))
        for topic in subject_data["topic"]:
            topic_prof_map.append([topic["name"], random.choice(topic["professors"]), topic["hours"]])
        return {"subject": subject_data["subject"], 
                "topic/professors": topic_prof_map, 
                "day": day, 
                "start_hour": start_hour, 
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
def generate_initial_population(subjects, professors_json, population_size):
    population = []
    for _ in range(population_size):
        schedule = {}
        for subject_id in subjects:
            new_schedule = generate_subject_schedule(subjects[subject_id], professors_json, schedule)
            while new_schedule is None:
                new_schedule = generate_subject_schedule(subjects[subject_id], professors_json, schedule)
            schedule[subject_id] = new_schedule
        population.append(schedule)
    return population

def hard_constraints(schedule):
    # No collision of schedules for the same professor in different subjects or modules
    professors_schedule = {}
    for subject_id in schedule:
        if "professor" in schedule[subject_id]:  # Regular subject
            professor = schedule[subject_id]["professor"]
            if professor in professors_schedule:
                if schedule_overlap(professors_schedule[professor], schedule[subject_id]):
                    return float('inf')  # Penalty for schedule collision
            professors_schedule[professor] = schedule[subject_id]
        elif "topic/professors" in schedule[subject_id]:  # Module
            for topic_info in schedule[subject_id]["topic/professors"]:
                professors = topic_info[1]  # Professor is at position 1 of the list
                if not isinstance(professors, list):
                    professors = [professors]  # Convert to list if single professor
                for professor in professors:
                    if professor in professors_schedule:
                        if schedule_overlap(professors_schedule[professor], schedule[subject_id]):
                            return float('inf')  # Penalty for schedule collision
                    professors_schedule[professor] = schedule[subject_id]
    # No collision of schedules for subjects or modules in the same semester in different subjects
    semesters_schedule = {}
    for subject_id in schedule:
        semester = subjects_json[subject_id]["semester"]
        if semester in semesters_schedule:
            if schedule_overlap(semesters_schedule[semester], schedule[subject_id]):
                return float('inf')  # Penalty for schedule collision
        semesters_schedule[semester] = schedule[subject_id]
    # No programming of groups between 13:00 and 15:00 from Monday to Friday
    for subject_id in schedule:
        day = schedule[subject_id]["day"]
        start_hour = schedule[subject_id]["start_hour"]
        duration = schedule[subject_id]["duration"]
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday"] and start_hour < 15 and start_hour + duration > 13:
            return float('inf')  # Penalty for scheduling groups in forbidden time
    # Subjects must be scheduled for no more than two hours per day and on pairs of days Monday-Thursday or Tuesday-Friday
    for subject_id in schedule:
        day = schedule[subject_id]["day"]
        duration = schedule[subject_id]["duration"]
        if duration > 2 or (day[0] not in ["monday", "tuesday"] or day[1] not in ["thursday", "friday"]):
            return float('inf')  # Penalty for exceeding hours or not scheduling on valid days
    # Respect the availability hours of professors
    for subject_id in schedule:
        professor = schedule[subject_id]["professor"]
        day = schedule[subject_id]["day"]
        start_hour = schedule[subject_id]["start_hour"]
        duration = schedule[subject_id]["duration"]
        professor_schedule = professors_json[professor]["schedule"]
        available_hours = [int(hour) for hour in professor_schedule[day[0]].split("-")]
        if start_hour < available_hours[0] or start_hour + duration > available_hours[1]:
            return float('inf')  # Penalty for scheduling outside of professor's availability
    # Respect the minimum and maximum values of workload assignment for professors
    for subject_id in schedule:
        professor = schedule[subject_id]["professor"]
        udc = subjects_json[subject_id].get("udc", 0)
        max_udc = professors_json[professor].get("maxUdc", float("inf"))
        assigned_udc = sum(subject_data["hours"] for subject_data in schedule.values() if "professor" in subject_data and subject_data["professor"] == professor)
        if assigned_udc + udc > max_udc:
            return float('inf')  # Penalty for exceeding maxUdc
    # A class cannot start at even hours unless the immediately higher odd hour has already been assigned to another professor
    for subject_id in schedule:
        start_hour = schedule[subject_id]["start_hour"]
        professor = schedule[subject_id]["professor"]
        if start_hour % 2 == 0 and start_hour + 1 not in [schedule[sub_id]["start_hour"] for sub_id in schedule if sub_id != subject_id and schedule[sub_id]["professor"] == professor]:
            return float('inf')  # Penalty for starting at even hour without odd hour assigned
    return 0

def soft_constraints(schedule):
    early_semester_penalty = sum(1 for subject_id in schedule if subjects_json[subject_id]["semester"] <= 2 and list(schedule[subject_id]["start_hour"])[0] + schedule[subject_id]["duration"] > 19) * 5
    return early_semester_penalty


def schedule_overlap(schedule1, schedule2):
    day_overlap = schedule1["day"] == schedule2["day"]
    hour_overlap = schedule1["start_hour"] < schedule2["start_hour"] + schedule2["duration"] and schedule1["start_hour"] + schedule1["duration"] > schedule2["start_hour"]
    return day_overlap and hour_overlap

# Function to evaluate a schedule based on hard and soft constraints
def evaluate_schedule(schedule):
    hard_score = hard_constraints(schedule)
    soft_score = soft_constraints(schedule)
    return hard_score, soft_score

# Function to select parents for crossover
def select_parents(population, tournament_size=3):
    selected_parents = []
    while len(selected_parents) < 2:
        tournament = random.sample(population, tournament_size)
        best_chromosome = min(tournament, key=lambda x: sum(evaluate_schedule(x)))
        selected_parents.append(best_chromosome)
    return selected_parents

# Function to perform crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child_schedule = {}
    for i, subject_id in enumerate(parent1):
        if i < crossover_point:
            child_schedule[subject_id] = parent1[subject_id]
        else:
            child_schedule[subject_id] = parent2[subject_id]
    return child_schedule

# Function to mutate a schedule
def mutate(schedule, mutation_rate=0.1):
    mutated_schedule = schedule.copy()
    for subject_id in mutated_schedule:
        if random.random() < mutation_rate:
            mutated_schedule[subject_id] = generate_subject_schedule(subjects_json[subject_id])
    return mutated_schedule

# Genetic algorithm
def genetic_algorithm(subjects, population_size, generations):
    population = generate_initial_population(subjects,professors_json, population_size)
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

# Main function
if __name__ == "__main__":
    subjects = subjects_json
    best_solution, best_scores = genetic_algorithm(subjects, population_size=5, generations=1)
    print("Best schedule:")
    for subject_id in best_solution:
        print(f"{subject_id}: {best_solution[subject_id]}")


