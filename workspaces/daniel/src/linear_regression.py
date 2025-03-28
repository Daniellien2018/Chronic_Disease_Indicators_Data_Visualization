import pandas as pd
from sklearn.linear_model import LinearRegression
from utils.model_evaluation import evaluate_model
from utils.model_saving import save_model

def load_data(file_path):
    """Load dataset from CSV."""
    return pd.read_csv(file_path)

def train_linear_regression(train_df):
    """Train a linear regression model."""
    # Select features and target variable - Use all features except the response
    X_train = train_df.drop('Mortality', axis=1) 
    y_train = train_df['Mortality']
    
    # Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model

def main():
    # Load train and test datasets
    train_df = load_data('data/processed/train.csv')
    test_df = load_data('data/processed/test.csv')
    
    # Train the Linear Regression model
    model = train_linear_regression(train_df)
    
    save_model(model, "linear_regression")

    # Evaluate the model
    mae, mse, rmse, r2 = evaluate_model(model, test_df)
    
    # Print the evaluation metrics
    print("Model Evaluation Metrics:")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R² (Coefficient of Determination): {r2}")

if __name__ == "__main__":
    main()
