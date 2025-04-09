# Data Cleaning, Splitting, Preprocessing
import pandas as pd
from sklearn.model_selection import train_test_split
from utils.util import one_hot_encoding

"""
Delete --> Not used 
Randomly splits the processed data into Train/Test using sklearn
"""
def load_data(file_path):
    """Load dataset from CSV."""
    df = pd.read_csv(file_path)
    return df

#Data is already processed 
def preprocess_data(df):
    """Preprocess the data (e.g., handle missing values, drop columns)."""
    # Example: Drop rows with missing target variable
    # df.dropna(subset=['Crude Prevalence (%)'], inplace=True)
    # You can add other preprocessing steps here as needed
    return df

def random_split(df, test_size=0.2, random_state=42):
    """Randomly split the data into training and testing sets."""
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    return train_df, test_df

def save_splits(train_df, test_df, train_file='data/processed/train.csv', test_file='data/processed/test.csv'):
    """Save the train and test splits to CSV files."""
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)

if __name__ == "__main__":
    # Load data
    file_path = 'data/raw/COPD2_0.csv'      
    df = load_data(file_path)
    
    # Preprocess data - Currently empty
    df = preprocess_data(df)

    # Apply one-hot encoding to categorical columns
    df = one_hot_encoding(df)

    # Split data (80% train, 20% test)
    train_df, test_df = random_split(df, test_size=0.2)
    
    # Save the splits to CSV
    save_splits(train_df, test_df)
    
    print("Data split and saved successfully!")