import pandas as pd

class DataFrameComparer:
    def __init__(self, merged_loc, udf_loc, key_column):
        self.merged_loc = merged_loc
        self.udf_loc = udf_loc
        self.key_column = key_column

    def find_differences(self):
        merged = pd.read_csv(self.merged_loc)
        udf = pd.read_csv(self.udf_loc)

        # Merge the two DataFrames on the key column
        merged_udf = pd.merge(merged, udf, on=self.key_column, how="outer", indicator=True)

        # Find rows that are in merged but not in udf
        merged_not_udf = merged_udf[merged_udf["_merge"] == "left_only"]

        # Find rows that are in udf but not in merged
        udf_not_merged = merged_udf[merged_udf["_merge"] == "right_only"]

        # Remove rows in udf but not in merged
        udf_cleaned = udf.merge(udf_not_merged, indicator='indicator', how='outer').query('indicator=="left_only"').drop(['indicator', '_merge', 'season'], axis=1)

        # Return the cleaned udf DataFrame and the list of original column names
        #print(merged_not_udf, udf_not_merged)
        return udf_cleaned, udf.columns.tolist()

# Example usage
merged_loc = "replic/season/season_merge.csv"
udf_loc = "replic/udf.csv"
key_column = "key"

comparer = DataFrameComparer(merged_loc, udf_loc, key_column)
udf_cleaned, udf_columns = comparer.find_differences()

# Save the cleaned udf DataFrame to a new CSV file with only the original column names from udf
udf_cleaned.to_csv("replic/udf_stage.csv", index=False, columns=udf_columns)
