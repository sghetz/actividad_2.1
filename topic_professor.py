import csv
import os
import json

class TopicCSVProcessor:
    def __init__(self, csv_folder, json_file):
        self.csv_folder = csv_folder
        self.json_file = json_file
        self.data = self.load_json()

    def load_json(self):
        with open(self.json_file, 'r') as f:
            return json.load(f)

    def process_csv_files(self):
        for filename in os.listdir(self.csv_folder):
            if filename.endswith('.csv'):
                key = os.path.splitext(filename)[0]  # Extract key from filename
                csv_path = os.path.join(self.csv_folder, filename)
                topics = self.extract_topics(csv_path)
                self.update_json(key, topics)

    def extract_topics(self, csv_path):
        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            topics = []
            for row in reader:
                topic_name = row['Name']
                topic_hours = row['Hours']
                professors = [key for key in row.keys() if key not in ['Topic', 'Name', 'Hours'] and row[key] == 'X']
                topics.append({'name': topic_name, 'hours': topic_hours, 'professors': professors})
            return topics

    def update_json(self, key, topics):
        self.data[key]['topic'] = topics

    def save_json(self):
        with open(self.json_file, 'w') as f:
            json.dump(self.data, f, indent=4)

# Path to the folder containing CSV files
csv_folder = 'replic\\module_topic_professor'
# Path to the JSON file
json_file = 'json\\udf.json'
processor = TopicCSVProcessor(csv_folder, json_file)
processor.process_csv_files()
processor.save_json()