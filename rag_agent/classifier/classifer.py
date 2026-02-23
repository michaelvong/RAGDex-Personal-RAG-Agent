# train_logistic_classifier.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sentence_transformers import SentenceTransformer
import joblib

# -------------------------------
# 1. Load Dataset
# -------------------------------
df = pd.read_csv('dataset.csv')  # replace with your filename if different

# Check dataset
print("Dataset sample:")
print(df.head())

queries = df['query'].tolist()
labels = df['label'].tolist()

# -------------------------------
# 2. Split into Train/Test
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    queries, labels, test_size=0.2, random_state=42, stratify=labels
)

# -------------------------------
# 3. Generate Embeddings
# -------------------------------
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
X_train_emb = embedding_model.encode(X_train, convert_to_numpy=True, show_progress_bar=True)
X_test_emb = embedding_model.encode(X_test, convert_to_numpy=True, show_progress_bar=True)

# -------------------------------
# 4. Train Logistic Regression
# -------------------------------
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_emb, y_train)

# -------------------------------
# 5. Evaluate
# -------------------------------
y_pred = clf.predict(X_test_emb)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -------------------------------
# 6. Save Models
# -------------------------------
joblib.dump(clf, "query_classifier.pkl")
joblib.dump(embedding_model, "embedding_model.pkl")

print("\nModels saved as 'query_classifier.pkl' and 'embedding_model.pkl'.")