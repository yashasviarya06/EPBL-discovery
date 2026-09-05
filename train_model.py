import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/opportunity_signals.csv")

print("Dataset loaded successfully!")
print(f"Total records: {len(df)}")


# ============================================================
# 2. SELECT INPUT AND TARGET
# ============================================================

X = df["signal_text"]
y = df["label"]


# ============================================================
# 3. SPLIT DATA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print(f"\nTraining records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")


# ============================================================
# 4. TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("\nTF-IDF transformation completed!")


# ============================================================
# 5. TRAIN MODEL
# ============================================================

model = LogisticRegression(
    random_state=42,
    max_iter=1000
)

model.fit(X_train_tfidf, y_train)

print("Logistic Regression model trained!")


# ============================================================
# 6. MAKE PREDICTIONS
# ============================================================

y_pred = model.predict(X_test_tfidf)


# ============================================================
# 7. EVALUATE MODEL
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================================
# 8. SAVE MODEL
# ============================================================

joblib.dump(model, "lead_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("\n==============================")
print("MODEL SAVED")
print("==============================")

print("lead_model.pkl")
print("tfidf_vectorizer.pkl")


# ============================================================
# 9. TEST WITH NEW OPPORTUNITIES
# ============================================================

new_signals = [
    "A new 900-unit residential township is planned near Pune with facilities for thousands of residents.",
    
    "A luxury beach resort with 250 rooms is proposed in Goa to support increasing tourism.",
    
    "A software company has opened a new technology office in Bengaluru.",
    
    "A new hospital campus with residential facilities is being developed in Maharashtra."
]


new_signals_tfidf = vectorizer.transform(new_signals)

predictions = model.predict(new_signals_tfidf)

probabilities = model.predict_proba(new_signals_tfidf)


print("\n==============================")
print("NEW LEAD PREDICTIONS")
print("==============================")


for text, prediction, probability in zip(
    new_signals,
    predictions,
    probabilities
):

    opportunity_score = probability[1] * 100

    if prediction == 1:
        result = "POTENTIAL OPPORTUNITY"
    else:
        result = "LOW PRIORITY / NOISE"

    print("\nSignal:")
    print(text)

    print(f"Prediction: {result}")
    print(f"Opportunity Score: {opportunity_score:.2f}%")