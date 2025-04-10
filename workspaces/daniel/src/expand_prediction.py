import pandas as pd
import numpy as np
import joblib
from utils.util import load_model


# Load your forecasted data (2021-2050 for states with Medicaid and Income)
forecasted_data = pd.read_csv("data/processed/forecasted_income_medicaid_by_state.csv")

original_df = pd.read_csv("data/raw/merged_raw_data.csv")

stratification_categories = original_df['Stratification'].unique()

# Define the stratification categories
# stratification_categories = ['Black - non-Hispanic', 'Female', 'White - non-Hispanic', 'Overall', 'Male']

expanded_rows = []
# Loop through each state and year in the forecasted data
for _, row in forecasted_data.iterrows():
    state = row['State']
    year = row['Year']
    medicaid_spending = row['Medicaid_Spending']
    median_income = row['Median_Income']
    
    # Add a row for each stratification category
    for strat in stratification_categories:
        expanded_rows.append({
            'Year': year,
            'State': state,
            'Stratification': strat,
            'Medicaid_Spending': medicaid_spending,
            'Median_Income': median_income
        })

# Create a new DataFrame from the expanded rows
expanded_df = pd.DataFrame(expanded_rows)

# Save the expanded DataFrame to a new CSV
expanded_df.to_csv("data/processed/expanded_mortality_data_2021_2050.csv", index=False)

print("✅ Stratification and expanded data saved to 'expanded_mortality_data_2021_2050.csv'")


