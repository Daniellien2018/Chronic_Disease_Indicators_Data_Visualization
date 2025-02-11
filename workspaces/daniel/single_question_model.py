"""
Given a single question saved as a csv, extract information and create a model
"""

import pandas as pd
def open_csv(path):
    return pd.read_csv(path)

def main(df):
    
    print(df.head())

def group_by_data_value_type(df):
    """
    Group the data by DataValueType.
    """
    # Group the data by 'DataValueType' and display the number of records in each group
    grouped_data = df.groupby('DataValueType')
    
    # Optionally: Print summary of the groups
    print("Group Summary:")
    for data_value_type, group in grouped_data:
        print(f"\nDataValueType: {data_value_type}")
        print(group.head())  # Print the first few rows for each group
    
    # Return the grouped data if needed for further processing
    return grouped_data


if __name__ == "__main__":
    csv_path = '/home/daniel.lien/dev/homework/data/cleaned_copd_data_question_COPD01.csv'
    df = open_csv(csv_path)
    group_by_data_value_type(df)
    # main(df)