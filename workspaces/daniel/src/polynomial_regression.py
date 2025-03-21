import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from utils.model_evaluation import evaluate_model
from utils.model_saving import save_model


def train_polynomial_regression(train_df, degree=2):
    """
    Train a polynomial regression model.
    :param train_df: Training dataframe
    :param degree: Degree of the polynomial features
    :return: Trained model
    """
    # Separate features and target
    X_train = train_df.drop('Prevalence', axis=1)
    y_train = train_df['Prevalence']

    # Create a polynomial regression pipeline
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train, y_train)

    return model

def main():
    # Load pre-processed data
    train_df = pd.read_csv('data/processed/train.csv')
    test_df = pd.read_csv('data/processed/test.csv')

    # Train polynomial regression model
    degree = 2  # Experiment with different polynomial degrees
    model = train_polynomial_regression(train_df, degree)

    # Save the model
    save_model(model, "polynomial_regression")

    # Evaluate the model
    mae, mse, rmse, r2 = evaluate_model(model, test_df)

    print("\nPolynomial Regression Model Evaluation:")
    print(f"Degree: {degree}")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")
    print(f"RMSE: {rmse}")
    print(f"R²: {r2}")

if __name__ == "__main__":
    main()
