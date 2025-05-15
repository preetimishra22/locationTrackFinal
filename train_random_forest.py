import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import pickle
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, top_k_accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load the training data
with open('user_location_history.json') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Encode categorical features
user_encoder = LabelEncoder()
day_encoder = LabelEncoder()
city_encoder = LabelEncoder()


df['user_enc'] = user_encoder.fit_transform(df['user'])
df['day_enc'] = day_encoder.fit_transform(df['day'])
df['city_enc'] = city_encoder.fit_transform(df['city'])

# Train the model
X = df[['user_enc', 'day_enc']]
y = df['city_enc']
# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict & evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 1. Accuracy
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.4f}")

# 2. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')

# Replace these with your actual city label names, in correct order
city_names = city_encoder.classes_  
plt.xticks(ticks=range(len(city_names)), labels=city_names, rotation=45)
plt.yticks(ticks=range(len(city_names)), labels=city_names, rotation=45)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# 3. Classification report (Precision, Recall, F1-score per class)
report = classification_report(y_test, y_pred, target_names=city_names)
print("Classification Report:\n", report)

# 4. Top-K Accuracy (Top-3 accuracy here)
# This requires probability outputs from the model (predict_proba)
y_proba = model.predict_proba(X_test)
top3_acc = top_k_accuracy_score(y_test, y_proba, k=3)
print(f"Top-3 Accuracy: {top3_acc:.4f}")


# Save model and encoders
with open('city_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('city_encoder.pkl', 'wb') as f:
    pickle.dump(city_encoder, f)

with open('day_encoder.pkl', 'wb') as f:
    pickle.dump(day_encoder, f)

with open('user_encoder.pkl', 'wb') as f:
    pickle.dump(user_encoder, f)