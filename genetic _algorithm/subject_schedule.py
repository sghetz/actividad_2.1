import random

# Definición de una materia y su horario asignado
class SubjectSchedule:
    def __init__(self, subject, day, start_hour, duration, professor):
        self.subject = subject
        self.day = day
        self.start_hour = start_hour
        self.duration = duration
        self.professor = professor

    def __repr__(self):
        return f"{self.subject} - {self.day} - {self.start_hour}-{self.start_hour+self.duration} - {self.professor}"

# Ejemplo de profesores
professors = ["Victor Manon", "Mauricio Paletta", "Juan Alvarado", "Roberto Leyva", "Yerly Flores"]

# Ejemplo de horarios
days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
start_hours = [7, 9, 11, 13, 15, 17]

# Generación de horarios aleatorios para una materia
def generate_subject_schedule(subject):
    day = random.choice(days)
    start_hour = random.choice(start_hours)
    duration = random.randint(1, 2) * 2  # Duración de 2 horas máximo por día
    professor = random.choice(professors)
    return SubjectSchedule(subject, day, start_hour, duration, professor)

# Ejemplo de uso
subject = "Object Oriented Programming"
schedule = generate_subject_schedule(subject)
print(schedule)
