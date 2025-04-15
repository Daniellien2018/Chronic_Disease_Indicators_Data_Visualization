from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline


def train_polynomial_regression(train_df, degree=2):
    """
    Train a polynomial regression model.
    :param train_df: Training dataframe
    :param degree: Degree of the polynomial features
    :return: Trained model
    """
    X_train = train_df.drop('Mortality', axis=1)
    y_train = train_df['Mortality']

    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train, y_train)

    return model