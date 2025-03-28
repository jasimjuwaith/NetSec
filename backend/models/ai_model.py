import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Define input CSV file (latest generated training data)
DATA_FILE = "data/training_data.csv"
MODEL_FILE = "backend/models/vpn_detection_model.pkl"

def load_data(file_path):
    """Load dataset and preprocess."""
    df = pd.read_csv(file_path)

    # Features used for classification
    features = [
        "bidirectional_packets", "bidirectional_bytes", 
        "bidirectional_mean_ps", "bidirectional_stddev_ps", 
        "bidirectional_mean_piat_ms", "bidirectional_stddev_piat_ms", 
        "bidirectional_syn_packets", "bidirectional_ack_packets", 
        "bidirectional_rst_packets", "splt_ps", "splt_piat_ms", "vpn_risk_score"
    ]

    # Target variable (VPN traffic: 1, Non-VPN: 0)
    target = "is_vpn"

    # Handle missing values
    df.fillna(0, inplace=True)

    X = df[features]
    y = df[target]

    # Scale features for better performance
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler

def train_vpn_detection_model():
    """Train and save a machine learning model for VPN detection."""
    print("🚀 Loading dataset...")
    X, y, scaler = load_data(DATA_FILE)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    print("🔍 Performing hyperparameter tuning...")
    model = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    print(f"✅ Best Model Parameters: {grid_search.best_params_}")

    # Cross-validation score
    cv_scores = cross_val_score(best_model, X, y, cv=5)
    print(f"📊 Cross-validation Accuracy: {np.mean(cv_scores):.4f}")

    # Evaluate on test data
    y_pred = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Test Accuracy: {accuracy:.4f}")
    print("📊 Classification Report:\n", classification_report(y_test, y_pred))

    # Save model & scaler for real-time inference
    joblib.dump({"model": best_model, "scaler": scaler}, MODEL_FILE)
    print(f"✅ Model saved at {MODEL_FILE}")

if __name__ == "__main__":
    train_vpn_detection_model()
