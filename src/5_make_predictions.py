import pandas as pd
import joblib

# ====================== FUNCTIONS ==========================

def load_model(model_path):
    """Load a trained model from file."""
    return joblib.load(model_path)

def load_data(data_path):
    """Load the expanded input DataFrame."""
    return pd.read_csv(data_path)

def one_hot_encode(df, columns_to_encode):
    """Apply one-hot encoding to specified columns."""
    return pd.get_dummies(df, columns=columns_to_encode, drop_first=True)

def predict_mortality(df, model):
    """Use trained model to predict mortality."""
    df['Mortality'] = model.predict(df)
    return df

def reverse_one_hot(df, prefix):
    """Reverse one-hot encoding for a given prefix (e.g., 'State_' or 'Stratification_')."""
    columns = [col for col in df.columns if col.startswith(prefix)]
    if not columns:
        return df  # No columns to reverse
    df[prefix.rstrip('_')] = df[columns].idxmax(axis=1).str.replace(prefix, '')
    return df, columns

def clean_final_columns(df, one_hot_cols_to_drop):
    """Keep only final needed columns."""
    columns_to_keep = ['Year', 'State', 'Stratification', 'Medicaid_Spending', 'Median_Income', 'Mortality']
    return df.drop(columns=one_hot_cols_to_drop)[columns_to_keep]

def save_predictions(df, output_path):
    """Save final DataFrame with predictions."""
    df.to_csv(output_path, index=False)
    print(f"✅ Mortality predictions saved to '{output_path}'")

# ======================== MAIN =============================

if __name__ == "__main__":
    # Define file paths
    model_path = "model_artifacts/random_forest.pkl"
    data_path = "data/predictors/forecasted_income_medicaid.csv"
    output_path = "outputs/COPD_predicted_mortality_2021_2050.csv"

    # Load model and data
    model = load_model(model_path)
    df = load_data(data_path)

    # One-hot encode categorical features
    df_encoded = one_hot_encode(df.copy(), ['State', 'Stratification'])

    # Predict mortality
    df_predicted = predict_mortality(df_encoded, model)

    # Reverse one-hot encoding to get readable columns
    df_predicted, state_cols = reverse_one_hot(df_predicted, 'State_')
    df_predicted, strat_cols = reverse_one_hot(df_predicted, 'Stratification_')

    # Drop one-hot columns and retain only desired columns
    df_clean = clean_final_columns(df_predicted, one_hot_cols_to_drop=state_cols + strat_cols)

    # Save final results
    save_predictions(df_clean, output_path)
