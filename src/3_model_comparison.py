import os
import pdb
import glob
import pandas as pd
from pathlib import Path
from utils.util import load_model
from utils.util import evaluate_model

"""
Compares the MAE, MSE, RMSE, R^2 for all models 
"""

def compare_models(model_names, test_df, model_dir='model_artifacts'):
    """Compare multiple models on the same test set."""
    results = []
    # Evaluate each model
    for model_name in model_names:
        print(f"Evaluating model: {model_name}")
        
        # Load the model
        model = load_model(model_name, model_dir)
        
        # Evaluate
        mae, mse, rmse, r2 = evaluate_model(model, test_df)
        
        # Store results
        results.append({
            'Model': model_name,
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R²': r2
        })

    # Display the results
    results_df = pd.DataFrame(results)
    print("\nModel Comparison Results:")
    print(results_df)

    # Save results as CSV for reference
    results_df.to_csv('evaluation/model_comparison_results.csv', index=False)
    print("\nModel comparison saved to 'evaluation/model_comparison_results.csv'")


def main():
    # Load the test dataset
    test_df = pd.read_csv('data/split/test.csv')

    # List of model names - Need to separate from paths
    model_dir = Path('model_artifacts/')
    # model_names = ['linear_regression', 'polynomial_regression', 'etc']
    model_names = [model.stem for model in model_dir.glob('*.pkl')]

    # Compare all models
    compare_models(model_names, test_df)

if __name__ == "__main__":
    main()
