import csv
import json

class SubjectCSVProcessor:
    def __init__(self, csv_file, json_data):
        self.csv_file = csv_file
        self.json_data = json_data

    def process_csv(self):
        with open(self.csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                subject_id = row['key']
                professors = [key for key in row.keys() if key != 'key' and row[key] == 'X']
                self.update_json(subject_id, professors)

    def update_json(self, subject_id, professors):
        if subject_id in self.json_data:
            self.json_data[subject_id]['Professors'] = professors

    def save_json(self, json_file):
        with open(json_file, 'w') as f:
            json.dump(self.json_data, f, indent=4)

# Example usage
json_file = 'json\\udf.json'
subject_csv_file = 'replic\\subject_professor.csv'

# Load existing JSON data
with open(json_file, 'r') as f:
    json_data = json.load(f)

# Process subjects CSV file
subject_processor = SubjectCSVProcessor(subject_csv_file, json_data)
subject_processor.process_csv()
subject_processor.save_json(json_file)
