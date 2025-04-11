from model_training.linear_regression import train_linear_regression
from model_training.polynomial_regression import train_polynomial_regression
from model_training.random_forest import train_random_forest
from model_training.gradient_descent import train_gradient_descent
from model_training.lasso_regression import train_lasso
from model_training.ridge_regression import train_ridge
from model_training.elastic_net import train_elastic_net

import pandas as pd
from utils.util import save_model
from utils.util import evaluate_model


def load_data(train_path='data/split/train.csv', test_path='data/split/test.csv'):
    """Load preprocessed train and test datasets"""
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    return train_df, test_df

def run_and_evaluate(model_name, train_fn, train_df, test_df, **kwargs):
    """Train, save, and evaluate a model."""
    print(f"\n=== Training {model_name} ===")
    model = train_fn(train_df, **kwargs)
    
    save_path = f"{model_name}"
    save_model(model, save_path)

    mae, mse, rmse, r2 = evaluate_model(model, test_df)
    print(f"\n{model_name.capitalize()} Evaluation:")
    print(f"MAE: {mae:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²: {r2:.4f}")


def main():
    train_df, test_df = load_data()

    run_and_evaluate("linear_regression", train_linear_regression, train_df, test_df)
    run_and_evaluate("polynomial_regression", train_polynomial_regression, train_df, test_df)
    run_and_evaluate("random_forest", train_random_forest, train_df, test_df)
    run_and_evaluate("gradient_descent", train_gradient_descent, train_df, test_df)
    run_and_evaluate("lasso_regression", train_lasso, train_df, test_df)
    run_and_evaluate("ridge_regression", train_ridge, train_df, test_df)
    run_and_evaluate("elastic_net", train_elastic_net, train_df, test_df)

if __name__ == "__main__":
    main()