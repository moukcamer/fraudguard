# ml/training/train_fraud_model.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pathlib import Path

# Simulate dataset (replace with real logs)
data = pd.DataFrame({
    'login_freq': [5, 20, 1, 50, 3],
    'new_device': [0, 1, 0, 1, 0],
    'night_login': [0, 1, 0, 1, 0],
    'msg_urgent': [0, 1, 0, 1, 0],
    'is_fraud': [0, 1, 0, 1, 0]
})

X = data.drop('is_fraud', axis=1)
y = data['is_fraud']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model
path = Path(__file__).parent.parent / 'models' / 'fraud_detector_v1.pkl'
path.parent.mkdir(exist_ok=True)
joblib.dump(model, path)
print(f"Model saved to {path}")