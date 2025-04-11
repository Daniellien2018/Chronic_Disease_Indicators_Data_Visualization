import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ====================== FORECASTING =========================

def load_data(file_path):
    """Load the historical dataset."""
    return pd.read_csv(file_path)

def train_model(X, y):
    """Train a linear regression model."""
    model = LinearRegression()
    model.fit(X, y)
    return model

def forecast_by_state(state_df, model, future_years):
    """Forecast medicaid spending and median income for a given state."""
    future_years_df = pd.DataFrame({"Year": future_years})
    preds = model.predict(future_years_df)
    return future_years_df, preds

def generate_forecast(df, future_years):
    """Generate the forecast for each state and both target columns."""
    forecast_list = []    

    for state in df["State"].unique():
        state_df = df[df["State"] == state].copy()
        temp_combined = None

        for target_col in ["Medicaid_Spending", "Median_Income"]:
            X = state_df[["Year"]]
            y = state_df[target_col]
            model = train_model(X, y)
            
            future_years_df, preds = forecast_by_state(state_df, model, future_years)
            
            temp = pd.DataFrame({
                "State": state,
                "Year": future_years,
                target_col: preds
            })

            if temp_combined is None:
                temp_combined = temp
            else:
                temp_combined = temp_combined.merge(temp, on=["State", "Year"])

        forecast_list.append(temp_combined)

    forecast_df = pd.concat(forecast_list, ignore_index=True)
    return forecast_df

# ===================== EXPANSION ===========================

def expand_forecast_by_stratification(forecast_df, stratification_categories):
    """Expand forecasted data across stratification categories."""
    expanded_rows = []

    for _, row in forecast_df.iterrows():
        for strat in stratification_categories:
            expanded_rows.append({
                'Year': row['Year'],
                'State': row['State'],
                'Stratification': strat,
                'Medicaid_Spending': row['Medicaid_Spending'],
                'Median_Income': row['Median_Income']
            })

    expanded_df = pd.DataFrame(expanded_rows)
    return expanded_df

if __name__ == "__main__":
    # Load your historical dataset (2000–2020)
    df = load_data("data/processed/merged_copd_income_medicaid.csv")
    
    # Forecast years
    future_years = np.arange(2021, 2051)
    
    # Generate forecast for all states
    forecast_df = generate_forecast(df, future_years)
    # Get stratificaiton categories to expand by ie ['Men', 'Women', 'Hispanic'...]
    stratification_categories = df['Stratification'].unique()

    expanded_forecast_df = expand_forecast_by_stratification(forecast_df, stratification_categories)

    output_file = 'data/predictors/forecasted_income_medicaid_by_stratification.csv'
    expanded_forecast_df.to_csv(output_file,index=False)
    print(f"✅ Forecast saved to '{output_file}'")
    

