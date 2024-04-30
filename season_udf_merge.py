import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Read the cleaned udf CSV file
udf_cleaned_loc = "replic/udf_stage.csv"
udf_cleaned = pd.read_csv(udf_cleaned_loc)

# Read the merged CSV file
merged_loc = "replic/season/season_merge.csv"
merged = pd.read_csv(merged_loc)

# Function to find the best match for a subject name in the udf DataFrame
def find_best_match(row):
    subject = row['subject']
    matches = process.extract(subject, udf_cleaned['subject'], limit=1, scorer=fuzz.token_sort_ratio)
    return matches[0][0]

# Apply the function to find the best match for each subject name in the merged DataFrame
merged['subject_match'] = merged.apply(find_best_match, axis=1)

# Merge the two DataFrames based on the best match for the "subject" column
merged_final = pd.merge(merged, udf_cleaned, left_on="subject_match", right_on="subject", how="left", suffixes=('_merged', '_udf'))

# Convert the 'hours' column to integer
merged_final['hours'] = merged_final['hours'].astype(int)

# Drop unnecessary columns
merged_final.drop(['subject_match', 'key_udf', 'subject_udf'], axis=1, inplace=True)

merged_final.rename(columns={"key_merged": "key", "subject_merged": "subject"}, inplace=True)

# Save the merged DataFrame to a new CSV file
merged_final.to_csv("replic/udf_final.csv", index=False)
