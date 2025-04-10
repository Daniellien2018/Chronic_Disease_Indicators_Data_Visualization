import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

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
    # Prepare the future DataFrame
    future_years_df = pd.DataFrame({"Year": future_years})
    
    # Predict for Medicaid_Spending and Median_Income
    preds = model.predict(future_years_df)
    
    return future_years_df, preds

def generate_forecast(df, future_years):
    """Generate the forecast for each state and both target columns."""
    forecast_list = []    

    # Loop through each state
    for state in df["State"].unique():
        state_df = df[df["State"] == state].copy()
        temp_combined = None

        # Loop through target columns (Medicaid_Spending, Median_Income)
        for target_col in ["Medicaid_Spending", "Median_Income"]:
            # Train model for the state
            X = state_df[["Year"]]
            y = state_df[target_col]
            model = train_model(X, y)
            
            # Forecast
            future_years_df, preds = forecast_by_state(state_df, model, future_years)
            
            # Store predictions in a temp DataFrame
            temp = pd.DataFrame({
                "State": state,
                "Year": future_years,
                target_col: preds
            })

            # Merge the predictions for both target columns
            if temp_combined is None:
                temp_combined = temp
            else:
                temp_combined = temp_combined.merge(temp, on=["State", "Year"])

        forecast_list.append(temp_combined)

    # Combine all states
    forecast_df = pd.concat(forecast_list, ignore_index=True)
    return forecast_df

def save_forecast(forecast_df, output_file):
    """Save the forecasted data to a CSV file."""
    forecast_df.to_csv(output_file, index=False)
    print(f"✅ Forecast saved to '{output_file}'")

if __name__ == "__main__":
    # Load your historical dataset (2000–2020)
    df = load_data("data/raw/merged_raw_data.csv")
    
    # Forecast years
    future_years = np.arange(2021, 2051)
    
    # Generate forecast for all states
    forecast_df = generate_forecast(df, future_years)
    
    # Save the forecast
    save_forecast(forecast_df, "data/processed/forecasted_income_medicaid_by_state.csv")
