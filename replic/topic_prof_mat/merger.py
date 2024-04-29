import os
import pandas as pd

# Path to the folder containing the CSV files
folder_path = "C:\\Users\\sghetz\\Desktop\\python_uni\\reto_palettowski\\replic\\topic_prof_mat"

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Iterate over each CSV file and append its data to the merged DataFrame
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    data = pd.read_csv(file_path)
    merged_data = pd.concat([merged_data, data], ignore_index=True)

# Save the merged data to a new CSV file
merged_data.to_csv('merged_data.csv', index=False)
