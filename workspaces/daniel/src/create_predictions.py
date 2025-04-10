import pandas as pd
import joblib


# Load the pre-trained random forest model
model = joblib.load('models/random_forest.pkl')

# Load the expanded DataFrame (which contains Year, State, Stratification, Medicaid_Spending, Median_Income)
expanded_df = pd.read_csv("data/processed/expanded_mortality_data_2021_2050.csv")

# One-hot encode the 'State' and 'Stratification' columns as they were in the model
expanded_df = pd.get_dummies(expanded_df, columns=['State', 'Stratification'], drop_first=True)

# Predict mortality using the trained model
expanded_df['Mortality'] = model.predict(expanded_df)  


# Reverse one-hot encoding for 'State'
state_columns = [col for col in expanded_df.columns if col.startswith('State_')]
expanded_df['State'] = expanded_df[state_columns].idxmax(axis=1).str.replace('State_', '')

# Reverse one-hot encoding for 'Stratification'
stratification_columns = [col for col in expanded_df.columns if col.startswith('Stratification_')]
expanded_df['Stratification'] = expanded_df[stratification_columns].idxmax(axis=1).str.replace('Stratification_', '')

# Drop the one-hot encoded columns
columns_to_keep = ['Year', 'State', 'Stratification', 'Medicaid_Spending', 'Median_Income', 'Mortality']
expanded_df = expanded_df[columns_to_keep]

# Save the updated DataFrame with predictions
expanded_df.to_csv("data/predictions/COPD_predicted_mortality_2021_2050.csv", index=False)

print("✅ Mortality predictions added and saved to 'COPD_predicted_mortality_2021_2050.csv'")
