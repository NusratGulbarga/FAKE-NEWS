import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import pickle
import os
import re

# Load datasets
true = pd.read_csv("True.csv")
fake = pd.read_csv("Fake.csv")

# Add labels
true['label'] = 1  # Real
fake['label'] = 0  # Fake

# Optional: Balance the data
fake = fake.sample(len(true), random_state=42)

# Combine and shuffle
df = pd.concat([true, fake])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Clean the text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)           # remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)  # remove junk chars
    return text.lower()

df['text'] = df['text'].apply(clean_text)

# Features & labels
X = df['text']
y = df['label']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Vectorize
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = PassiveAggressiveClassifier(max_iter=1000)
model.fit(X_train_vec, y_train)

# Save model & vectorizer
os.makedirs("model", exist_ok=True)
with open("model/fake_news_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Model trained and saved to model/fake_news_model.pkl")

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Predict on test data
y_pred = model.predict(X_test_vec)

# Evaluation
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("📋 Classification Report:\n", classification_report(y_test, y_pred))
