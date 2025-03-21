
import pdb
import pandas as pd
from utils.model_saving import load_model
from utils.model_evaluation import evaluate_model

"""
NOT WORKING YET 3/18
"""
def compare_models(model_names, test_df, model_dir='../daniel/models'):
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
    results_df.to_csv('data/model_results/model_comparison_results.csv', index=False)
    print("\nModel comparison saved to '/data/model_results/model_comparison_results.csv'")


def main():
    # Load the test dataset
    # this test df is not one-hot coded
    # the model i read in is one-hot coded 
    test_df = pd.read_csv('data/processed/test.csv')

    # List of model names (use the names you saved them with)
    model_names = ['linear_regression', 'polynomial_regression']

    # Compare all models
    compare_models(model_names, test_df)

if __name__ == "__main__":
    main()
