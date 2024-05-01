import os
import pandas as pd
import json

class CSVParser:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def read_and_parse_csv(self):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(self.csv_file)

        # Replace NaN values with "null"
        df.fillna(value='null', inplace=True)

        # Check if "P1", "P2", and "P3" columns exist and create "period" key if they do
        if all(col in df.columns for col in ["P1", "P2", "P3"]):
            pattern_mapping = {
                "PMT1": ["X", "null", "null"],
                "PMT2": ["null", "X", "null"],
                "PMT3": ["null", "null", "X"],
                "PMT4": ["X", "X", "null"],
                "PMT5": ["null", "X", "X"],
                "PMT6": ["X", "X", "X"]
            }
            df["period"] = df[["P1", "P2", "P3"]].apply(lambda x: [key for key, val in pattern_mapping.items() if val == x.tolist()][0] if x.tolist() in pattern_mapping.values() else x, axis=1)
            df.drop(columns=["P1", "P2", "P3"], inplace=True)

        
        if "maxUdc" in df.columns:
            df["maxUdc"] = pd.to_numeric(df["maxUdc"], errors='coerce').fillna(0).astype(int)

        if "payroll" in df.columns:
            # Set the "payroll" column as the index
            df.set_index("payroll", inplace=True)

        # Convert the DataFrame to a dictionary with "payroll" as keys
        data_dict = df.to_dict(orient='index')

        return data_dict

    def convert_to_json(self, json_file):
        # Read and parse the availability data from the CSV file
        availability_data = self.read_and_parse_csv()
        j = json.dumps(availability_data, indent=4, default=str)
        with open(json_file, 'w+') as f:
            print(j, file=f)
    
    def modify_udf_json_keys(self, json_file):
        # Read the JSON file
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Create a new dictionary with updated keys
        updated_data = {data[key]["key"]: {k: v for k, v in data[key].items() if k != "key"} for key in data}

        # Write the updated data back to the JSON file
        with open(json_file, 'w') as f:
            json.dump(updated_data, f, indent=4, default=str)

# Example CSV file
current_dir = os.getcwd()
professor_csv = os.path.join(current_dir, "replic\\professor.csv")
udf_csv = os.path.join(current_dir, "replic\\udf_final.csv")

# Create an instance of CSVParser and use it to convert the CSV files to JSON
professor_csv_parsed = CSVParser(professor_csv)
professor_csv_parsed.convert_to_json('json\\professor.json')

udf_csv_parsed = CSVParser(udf_csv)
udf_csv_parsed.convert_to_json('json\\udf.json')
udf_csv_parsed.modify_udf_json_keys('json\\udf.json')
