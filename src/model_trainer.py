"""
Machine Learning Model Development and Evaluation Pipeline.
Trains, compares, and evaluates multiple document classification algorithms:
1. Logistic Regression
2. Multinomial Naive Bayes
3. Linear Support Vector Machine
4. Random Forest Classifier
Saves the best performing model, vectorizer, and evaluation reports.
"""
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.pipeline import Pipeline

def train_and_evaluate_models(data_path="data/dataset.csv", models_dir="models"):
    print(f"Loading preprocessed dataset from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Explicitly convert to standard Python list / numpy ndarray of objects
    X = np.array(df["cleaned_text"].astype(str).tolist(), dtype=object)
    y = np.array(df["category"].astype(str).tolist(), dtype=object)
    
    # Stratified train/test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training set size: {len(X_train)} | Test set size: {len(X_test)}")
    
    # Candidate classifiers
    candidate_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, C=1.0, random_state=42),
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.1),
        "Linear Support Vector Machine": LinearSVC(random_state=42, dual="auto"),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = []
    trained_pipelines = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    print("\n--- Evaluating Models with 5-Fold Cross Validation ---")
    for name, clf in candidate_models.items():
        pipe = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=2500, sublinear_tf=True)),
            ("clf", clf)
        ])
        
        # Cross validation scores
        scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="accuracy")
        mean_cv = float(scores.mean())
        std_cv = float(scores.std())
        
        # Fit on training split
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        
        test_acc = float(accuracy_score(y_test, y_pred))
        test_f1 = float(f1_score(y_test, y_pred, average="weighted"))
        
        results.append({
            "Model": name,
            "CV_Accuracy_Mean": mean_cv,
            "CV_Accuracy_Std": std_cv,
            "Test_Accuracy": test_acc,
            "Test_F1_Weighted": test_f1
        })
        trained_pipelines[name] = pipe
        print(f"[{name}] 5-Fold CV Acc: {mean_cv*100:.2f}% (+/- {std_cv*100:.2f}%) | Test Acc: {test_acc*100:.2f}% | Test F1: {test_f1:.4f}")

    results_df = pd.DataFrame(results).sort_values(by="Test_F1_Weighted", ascending=False)
    print("\nModel Comparison Table:")
    print(results_df.to_string(index=False))

    # Pick the best model
    best_model_name = results_df.iloc[0]["Model"]
    best_pipeline = trained_pipelines[best_model_name]
    print(f"\nSelected Best Model: {best_model_name}")

    # Detailed test evaluation on the best model
    y_pred_best = best_pipeline.predict(X_test)
    labels = sorted(list(set(y)))
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred_best, target_names=labels))

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred_best, labels=labels)
    cm_df = pd.DataFrame(cm, index=[f"Actual {l}" for l in labels], columns=[f"Pred {l}" for l in labels])
    print(cm_df)

    # Save artifacts
    os.makedirs(models_dir, exist_ok=True)
    model_file = os.path.join(models_dir, "document_classifier.pkl")
    vectorizer_file = os.path.join(models_dir, "tfidf_vectorizer.pkl")
    metadata_file = os.path.join(models_dir, "model_metadata.pkl")

    joblib.dump(best_pipeline.named_steps["clf"], model_file)
    joblib.dump(best_pipeline.named_steps["tfidf"], vectorizer_file)
    
    metadata = {
        "best_model_name": best_model_name,
        "classes": labels,
        "comparison_results": results_df.to_dict(orient="records"),
        "confusion_matrix": cm.tolist(),
        "test_accuracy": float(results_df.iloc[0]["Test_Accuracy"]),
        "test_f1": float(results_df.iloc[0]["Test_F1_Weighted"])
    }
    joblib.dump(metadata, metadata_file)
    print(f"\nSuccessfully saved trained model and vectorizer into '{models_dir}/'!")

if __name__ == "__main__":
    train_and_evaluate_models()
