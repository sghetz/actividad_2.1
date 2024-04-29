import os
import pandas as pd

def parse_availability(input_string):
    # Convert input_string to a string (in case it's a float or other type)
    input_string = str(input_string)
    
    # Split the input string into tokens
    tokens = input_string.split(' ')
    availability = {}

    # Iterate over tokens to extract time ranges and days
    i = 0
    while i < len(tokens):
        if tokens[i].isdigit() and i + 2 < len(tokens) and tokens[i + 1] == 'to' and tokens[i + 2].isdigit():
            # Extract the start and end times of the range
            start_time = int(tokens[i])
            end_time = int(tokens[i + 2])

            # Generate the list of hours in the range
            hours = list(range(start_time, end_time + 1))
            
            # Check if the key for the current day exists in the dictionary
            if i + 4 < len(tokens) and tokens[i + 4] not in availability:
                availability[tokens[i + 4]] = []
            
            # Add the hours to the availability dictionary for the current day
            if i + 4 < len(tokens):
                availability[tokens[i + 4]] += hours

            # Increment i by 5 to skip to the next day
            i += 5
        else:
            i += 1

    # Return the availability schedule as a dictionary
    return availability



def read_and_parse_availability_from_csv(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Iterate over rows in the DataFrame
    for index, row in df.iterrows():
        # Parse the schedule field for each row
        availability_schedule = parse_availability(row['schedule'])

        # Add the parsed availability schedule to the dictionary
        row['availability'] = availability_schedule

    # Convert the DataFrame to a list of dictionaries
    data_dict = df.to_dict(orient='records')

    return data_dict

# Example CSV file

dirname = os.path.dirname(__file__)
csv_file = os.path.join(dirname, "professor.csv")

csv_file = "C:\\Users\\sghet\\OneDrive\\Desktop\\reto_papaletowski\\replic\\professor.csv"

# Read and parse the availability data from the CSV file
availability_data = read_and_parse_availability_from_csv(csv_file)
print(availability_data)

