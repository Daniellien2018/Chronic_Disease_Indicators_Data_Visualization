import os
import joblib

def save_model(model, model_name, model_dir='../daniel/models'):
    """Save the trained model to disk."""
    os.makedirs(model_dir, exist_ok=True) 
    model_path = os.path.join(model_dir, f"{model_name}.pkl")
    
    joblib.dump(model, model_path)
    print(f"Model saved at: {model_path}")

def load_model(model_name, model_dir='../models'):
    """Load a saved model from disk."""
    model_path = os.path.join(model_dir, f"{model_name}.pkl")
    
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print(f"Model loaded from: {model_path}")
        return model
    else:
        raise FileNotFoundError(f"Model {model_name} not found in {model_dir}")
