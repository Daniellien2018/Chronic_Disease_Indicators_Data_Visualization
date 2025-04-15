from sklearn.linear_model import ElasticNet

def train_elastic_net(train_df):
    """Train an Elastic Net regression model."""
    X_train = train_df.drop('Mortality', axis=1)
    y_train = train_df['Mortality']
    
    model = ElasticNet(alpha=0.1, l1_ratio=0.5)
    model.fit(X_train, y_train)
    
    return model