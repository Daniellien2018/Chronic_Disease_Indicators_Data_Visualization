"""
Dataset Cleaning for Chronic Obstructive Pulmonary Disease (COPD)
"""

import pandas as pd
import pdb
from pathlib import Path

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
            'TopicID', 'DataValueTypeID', 'DataSource', 'Topic', 'LowConfidenceLimit', 'HighConfidenceLimit', 'YearEnd']
df = df.drop(columns=columns_to_drop)


## Specific Cleaning
"""TODO
Remove non states from LocationDes c = ["Virgin Islands", "Puerto Rico", "Guam", "District of Columbia","United States"]
Handle missing values in DataValue ~30%
"""
# Step 4: Identify and handle missing values 
# ~30% of data is missing in the 'DataValue' column, so let's remove those rows
df = df.dropna(subset=['DataValue'])

# Remove non-state locations
states_to_keep = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", 
                  "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", 
                  "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
                  "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", 
                  "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
                  "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

df = df[df['LocationDesc'].isin(states_to_keep)]


# Step 5: Group into 6 dataframes based on "QuestionID"
questions = df['Question'].unique()
df_grouped = {}

for question in questions:
    df_grouped[question] = df[df['Question'] == question].reset_index(drop=True)

# View head of each dataframe formatted nicely 
for question, group in df_grouped.items():
    print(f"Question: {question}")
    print(group.head()) 

# Step 6: Reset Index for each dataframe
for question, group in df_grouped.items():
    df_grouped[question].reset_index(drop=True, inplace=True)


QUESTION_MAP = {
    "Chronic obstructive pulmonary disease among adults" : "COPD01",
    "Current smoking among adults with chronic obstructive pulmonary disease" : "COPD02",
    "Hospitalization for chronic obstructive pulmonary disease as any diagnosis, Medicare-beneficiaries aged 65 years and older" : "COPD03",
    "Hospitalization for chronic obstructive pulmonary disease as principal diagnosis, Medicare-beneficiaries aged 65 years and older" : "COPD04",
    "Chronic obstructive pulmonary disease mortality among adults aged 45 years and older, underlying cause" : "COPD05",
    "Chronic obstructive pulmonary disease mortality among adults aged 45 years and older, underlying or contributing cause" : "COPD06"

}
# Step 7: Save the cleaned dataset by question number
for i, (question, group) in enumerate(df_grouped.items(), 1):
    question_id = QUESTION_MAP[question]
    file_name = f"/home/daniel.lien/dev/homework/data/cleaned_copd_data_question_{question_id}.csv"
    group.to_csv(file_name, index=False)
    print(f"Saved cleaned data for question {i} as {file_name}")

print("Data cleaning complete. Cleaned datasets saved as 'cleaned_copd_data_question_X.csv'.")



# # Step 6: Reset Index for each 
# df.reset_index(drop=True, inplace=True)

# # Step 7: Save the cleaned dataset by question num
# df.to_csv("/home/daniel.lien/dev/homework/data/cleaned_copd_data.csv", index=False)

# print("Data cleaning complete. Cleaned dataset saved as 'cleaned_copd_data.csv'.")
