"""
Dataset Cleaning for Chronic Obstructive Pulmonary Disease (COPD)
"""

from pathlib import Path
import pandas as pd

#input your relative path here 
rel_path = Path("/home/daniel.lien/dev/homework/data/")
dataset_csv = Path("U.S._Chronic_Disease_Indicators_20250204.csv")


## General Cleaning
# Step 1: Read in Data
df = pd.read_csv(rel_path / dataset_csv)

# Step 2: Filter The Data for COPD-related records
df = df[df['Topic'] == 'Chronic Obstructive Pulmonary Disease']

# Step 3: Drop Uncessesary Columns - 
columns_to_drop = ['Response','ResponseID',
            'Stratification2','StratificationCategory2','StratificationID2','StratificationCategoryID2',
            'Stratification3', 'StratificationCategory3', 'StratificationID3','StratificationCategoryID3',
            'DataValueAlt', 'DataValueFootnoteSymbol', 'DataValueFootnote','LocationID', 'LocationAbbr',
            'TopicID', 'DataValueTypeID']
df = df.drop(columns=columns_to_drop)


## Specific Cleaning
"""TODO
Remove non states from LocationDesc = ["Virgin Islands", "Puerto Rico", "Guam", "District of Columbia","United States"]
Handle missing values in DataValue ~30%
"""
# Step 4: Identify and handle missing values 
# missing_values = df.isnull().sum()
# print("Missing values per column:\n", missing_values)
# ~30% of data is missing 

"""2/4
For now, skip all missing data so i can understand each row first 
"""
# Step 6: Reset Index
df.reset_index(drop=True, inplace=True)

# Step 7: Save the cleaned dataset
df.to_csv("/home/daniel.lien/dev/homework/data/cleaned_copd_data.csv", index=False)

print("Data cleaning complete. Cleaned dataset saved as 'cleaned_copd_data.csv'.")
