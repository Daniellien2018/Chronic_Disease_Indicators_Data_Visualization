from sklearn.linear_model import Lasso

def train_lasso(train_df):
    """Train a Lasso regression model."""
    X_train = train_df.drop('Mortality', axis=1)
    y_train = train_df['Mortality']
    
    model = Lasso(alpha=0.1)
    model.fit(X_train, y_train)
    
    return model