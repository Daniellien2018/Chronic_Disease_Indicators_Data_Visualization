import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def train_random_forest(train_df):
    """Train a Random Forest regression model."""
    X_train = train_df.drop('Mortality', axis=1)
    y_train = train_df['Mortality']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model

