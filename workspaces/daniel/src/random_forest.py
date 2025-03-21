import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from utils.model_evaluation import evaluate_model
from utils.model_saving import save_model


def load_data(file_path):
    """Load dataset from CSV."""
    return pd.read_csv(file_path)

def train_random_forest(train_df):
    """Train a Random Forest regression model."""
    X_train = train_df.drop('Prevalence', axis=1)
    y_train = train_df['Prevalence']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model

def main():
    train_df = load_data('data/processed/train.csv')
    test_df = load_data('data/processed/test.csv')

    model = train_random_forest(train_df)

    save_model(model, 'random_forest')

    mae, mse, rmse, r2 = evaluate_model(model, test_df)

    print("Random Forest Regression Evaluation Metrics:")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")
    print(f"RMSE: {rmse}")
    print(f"R²: {r2}")


if __name__ == "__main__":
    main()