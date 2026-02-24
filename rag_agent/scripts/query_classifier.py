import joblib

# Load trained models
clf = joblib.load(r"C:\Users\Michael\PycharmProjects\PersonalRAG\rag_agent\classifier\query_classifier.pkl")
embedding_model = joblib.load(r"C:\Users\Michael\PycharmProjects\PersonalRAG\rag_agent\classifier\embedding_model.pkl")


def classify_query(query: str, threshold=0.5):
    # Embed the query
    emb = embedding_model.encode([query], convert_to_numpy=True)

    # Get predicted label and probabilities
    probs = clf.predict_proba(emb)[0]  # shape = [n_classes]
    classes = clf.classes_  # ['general', 'retrieval']

    # Choose the class with highest probability
    max_idx = probs.argmax()
    label = classes[max_idx]
    confidence = probs[max_idx]

    # Optional: enforce a threshold for retrieval
    if confidence < threshold:
        label = "general"  # fallback if classifier isn't confident

    return label, confidence


# Example usage
query = "What projects can I build with AWS"
label, confidence = classify_query(query)
print(f"Label: {label}, Confidence: {confidence:.2f}")

# Conditional retrieval
if label == "retrieval":
    print("Do Chroma DB retrieval + RAG")
else:
    print("Directly answer with LLM")