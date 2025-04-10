import pandas as pd
from sklearn.linear_model import ElasticNet
from utils.model_evaluation import evaluate_model
from utils.model_saving import save_model

def load_data(file_path):
    """Load dataset from CSV."""
    return pd.read_csv(file_path)

def train_elastic_net(train_df):
    """Train an Elastic Net regression model."""
    X_train = train_df.drop('Mortality', axis=1)
    y_train = train_df['Mortality']
    
    model = ElasticNet(alpha=0.1, l1_ratio=0.5)  # l1_ratio controls L1 vs. L2 mix
    model.fit(X_train, y_train)
    
    return model

def main():
    train_df = load_data('data/processed/train.csv')
    test_df = load_data('data/processed/test.csv')
    
    model = train_elastic_net(train_df)
    
    save_model(model, "elastic_net")

    mae, mse, rmse, r2 = evaluate_model(model, test_df)

    print("Elastic Net Regression Evaluation Metrics:")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")
    print(f"RMSE: {rmse}")
    print(f"R²: {r2}")

if __name__ == "__main__":
    main()
