import json
import re

class ScheduleTranslator:
    def __init__(self):
        pass

    def translate(self, schedule):
        if schedule == "null" or schedule == "Flexible":
            return self.default_schedule()
        elif " / " in schedule:
            return self.handle_slash_schedule(schedule)
        else:
            return self.handle_regular_schedule(schedule)

    def default_schedule(self):
        return {
            "monday": "7-21",
            "tuesday": "7-21",
            "wednesday": "7-21",
            "thursday": "7-21",
            "friday": "7-21"
        }
        '''return {
            "Monday": "7:00-9:00,9:00-11:00,11:00-13:00,13:00-15:00,15:00-17:00,17:00-19:00,19:00-21:00",
            "Tuesday": "7:00-9:00,9:00-11:00,11:00-13:00,13:00-15:00,15:00-17:00,17:00-19:00,19:00-21:00",
            "Wednesday": "7:00-9:00,9:00-11:00,11:00-13:00,13:00-15:00,15:00-17:00,17:00-19:00,19:00-21:00",
            "Thursday": "7:00-9:00,9:00-11:00,11:00-13:00,13:00-15:00,15:00-17:00,17:00-19:00,19:00-21:00",
            "Friday": "7:00-9:00,9:00-11:00,11:00-13:00,13:00-15:00,15:00-17:00,17:00-19:00,19:00-21:00"
        }'''

    def handle_slash_schedule(self, schedule):
        pattern = r'(\d{1,2}) to (\d{1,2}) \/ (\d{1,2}) to (\d{1,2}) ((?:Mon|Tue|Wed|Thu|Fri)+)'
        slots = re.findall(pattern, schedule)
        translated_schedule = {}
        for start_l, end_l, start_r, end_r, days_str in slots:
            day = {'Mon': 'monday', 'Tue': 'tuesday', 'Wed': 'wednesday', 'Thu': 'thursday', 'Fri': 'friday'}
            for day_abbr in re.findall(r'\w{3}', days_str):
                full_day = day[day_abbr]
                if full_day not in translated_schedule:
                    translated_schedule[full_day] = []
                translated_schedule[full_day].append(f"{start_l}-{end_l}")
                translated_schedule[full_day].append(f"{start_r}-{end_r}")

        for day in translated_schedule:
            translated_schedule[day] = ', '.join(translated_schedule[day])

        return translated_schedule

    def handle_regular_schedule(self, schedule):
        days_times = re.findall(r'(\d{1,2}) to (\d{1,2}) ((?:Mon|Tue|Wed|Thu|Fri)+)', schedule)
        translated_schedule = {}
        for start, end, days_str in days_times:
            days = {'Mon': 'monday', 'Tue': 'tuesday', 'Wed': 'wednesday', 'Thu': 'thursday', 'Fri': 'friday'}
            for day_abbr in re.findall(r'\w{3}', days_str):
                day = days[day_abbr]
                if day not in translated_schedule:
                    translated_schedule[day] = []
                translated_schedule[day].append(f"{start}-{end}")

        for day in translated_schedule:
            translated_schedule[day] = ', '.join(translated_schedule[day])

        return translated_schedule

# Usage
translator = ScheduleTranslator()

with open('json\\professor.json') as json_file:
    data = json.load(json_file)

for key, value in data.items():
    value["schedule"] = translator.translate(value["schedule"])

# Save to a new file
with open('json\\professor_final.json', 'w+') as outfile:
    json.dump(data, outfile, indent=4)
