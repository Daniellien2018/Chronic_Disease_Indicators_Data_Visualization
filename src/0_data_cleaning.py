import re
import pandas as pd

# ----------------------------------------
# Load and Clean COPD Mortality Data
# ----------------------------------------

copd_path = 'data/raw/U.S._Chronic_Disease_Indicators__CDI___2023_Release copy.csv'
df_copd = pd.read_csv(copd_path)

# Drop completely empty or unnecessary columns
drop_cols_copd = [
    'Response', 'StratificationCategory2', 'Stratification2',
    'StratificationCategory3', 'Stratification3', 'ResponseID',
    'StratificationCategoryID2', 'StratificationID2', 'StratificationCategoryID3',
    'StratificationID3', 'YearEnd', 'LocationAbbr', 'DataSource',
    'DataValueAlt', 'DataValueFootnoteSymbol', 'DatavalueFootnote',
    'HighConfidenceLimit', 'LowConfidenceLimit', 'LocationID',
    'DataValueTypeID', 'TopicID'
]
df_copd.drop(columns=drop_cols_copd, inplace=True)

# Filter COPD-specific rows
df_copd = df_copd[df_copd['Topic'] == 'Chronic Obstructive Pulmonary Disease']

states_to_keep = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]
df_copd = df_copd[df_copd['LocationDesc'].isin(states_to_keep)]

# Drop more unnecessary columns
df_copd.drop(columns=[
    'Topic', 'GeoLocation', 'QuestionID', 'StratificationCategoryID1',
    'StratificationID1', 'DataValueUnit', 'StratificationCategory1'
], inplace=True)

# Keep only mortality count rows
df_copd = df_copd[
    (df_copd['DataValueType'] == 'Number') &
    (df_copd['Question'] == 'Mortality with chronic obstructive pulmonary disease as underlying or contributing cause among adults aged >= 45 years')
]

df_copd.dropna(inplace=True)
df_copd.drop(columns=['DataValueType'], inplace=True)

# Rename and clean columns
df_copd.rename(columns={
    'YearStart': 'Year',
    'LocationDesc': 'State',
    'DataValue': 'Mortality',
    'Stratification1': 'Stratification'
}, inplace=True)

df_copd = df_copd[df_copd['Year'] != 2010]
df_copd.sort_values(['State', 'Year'], inplace=True)

# ----------------------------------------
# Load and Clean Medicaid Spending Data
# ----------------------------------------

medicaid_path = 'data/raw/MEDICAID_AGGREGATE20.CSV'
df_medicaid = pd.read_csv(medicaid_path)

# Drop unnecessary columns
drop_cols_medicaid = [
    'Code', 'Region_Number', 'Region_Name', 'Average_Annual_Percent_Growth'
] + [f'Y{y}' for y in range(1991, 2011)]
df_medicaid.drop(columns=drop_cols_medicaid, inplace=True)

df_medicaid = df_medicaid[df_medicaid['Group'] == 'State']
df_medicaid = df_medicaid[df_medicaid['State_Name'] != 'District of Columbia']
df_medicaid.dropna(inplace=True)

# Convert year columns to numeric
year_cols = [col for col in df_medicaid.columns if col.startswith('Y')]
df_medicaid[year_cols] = df_medicaid[year_cols].apply(pd.to_numeric, errors='coerce')

# Melt to long format
df_medicaid_long = df_medicaid.melt(
    id_vars=['State_Name'], value_vars=year_cols,
    var_name='Year', value_name='Medicaid_Spending'
)

# Convert 'Year' to integer
df_medicaid_long['Year'] = df_medicaid_long['Year'].str.extract('(\\d+)').astype(int)

# Group in case of duplicates (unlikely)
df_medicaid_cleaned = df_medicaid_long.groupby(['State_Name', 'Year'])['Medicaid_Spending'].sum().reset_index()
df_medicaid_cleaned.rename(columns={'State_Name': 'State'}, inplace=True)

# ----------------------------------------
# Load and Clean Median Income Data
# ----------------------------------------

income_path = 'data/raw/h08.xlsx'
df_income = pd.read_excel(income_path, skiprows=7)

# Remove unnamed columns and extract years
df_income.columns = df_income.columns.map(str)
df_income = df_income.loc[:, ~df_income.columns.str.contains('^Unnamed')]

years_to_drop = ['2017 (40)', '2013 (39)'] # Drop Uneccesary Years
df_income = df_income.drop(columns=years_to_drop)

def extract_year(col):
    match = re.search(r'\b(19|20)\d{2}\b', str(col))
    return match.group(0) if match else col

df_income.columns = [extract_year(col) for col in df_income.columns]

# Keep relevant columns
years_to_keep = [str(y) for y in range(2011, 2021)]
columns_to_keep = ['State'] + years_to_keep
df_income = df_income[columns_to_keep]

# Clean up rows
df_income = df_income[~df_income['State'].isin(['United States', 'District of Columbia'])]
df_income = df_income.iloc[:51]  # Keep first 50 states

df_income = df_income.drop(index=0) #drop first row header 

# Melt to long format
df_income_long = df_income.melt(id_vars='State', var_name='Year', value_name='Median_Income')
df_income_long['Year'] = df_income_long['Year'].astype(int)

# ----------------------------------------
# Merge All Datasets
# ----------------------------------------

# Merge income into COPD
df_merged = df_copd.merge(df_income_long, on=['State', 'Year'], how='left')

# Merge Medicaid spending
df_merged = df_merged.merge(df_medicaid_cleaned, on=['State', 'Year'], how='left')

# Final cleanup and column selection
df_merged = df_merged.drop(columns='Question')
df_merged = df_merged[['Year', 'State', 'Stratification', 'Medicaid_Spending', 'Median_Income', 'Mortality']]

# Output merged dataset
output_path = 'data/processed/merged_copd_income_medicaid.csv'
df_merged.to_csv(output_path, index=False)

print(f"Preprocessing complete. Data saved to {output_path}")
