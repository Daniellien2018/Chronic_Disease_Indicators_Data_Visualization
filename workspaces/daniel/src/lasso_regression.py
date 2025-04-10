import pandas as pd
from sklearn.linear_model import Lasso
from utils.model_evaluation import evaluate_model
from utils.model_saving import save_model

def load_data(file_path):
    """Load dataset from CSV."""
    return pd.read_csv(file_path)

def train_lasso(train_df):
    """Train a Lasso regression model."""
    X_train = train_df.drop('Mortality', axis=1)
    y_train = train_df['Mortality']
    
    model = Lasso(alpha=0.1)  # Alpha controls the sparsity
    model.fit(X_train, y_train)
    
    return model

def main():
    train_df = load_data('data/processed/train.csv')
    test_df = load_data('data/processed/test.csv')
    
    model = train_lasso(train_df)
    
    save_model(model, "lasso")

    mae, mse, rmse, r2 = evaluate_model(model, test_df)

    print("Lasso Regression Evaluation Metrics:")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")
    print(f"RMSE: {rmse}")
    print(f"R²: {r2}")

if __name__ == "__main__":
    main()
