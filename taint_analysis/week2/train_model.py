# train_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import OneHotEncoder

def main():
    features_path = "features.csv"
    labels_path = "labels.csv" # You must create this file manually!
    model_output_path = "model.pkl"

    try:
        features_df = pd.read_csv(features_path)
        labels_df = pd.read_csv(labels_path)
    except FileNotFoundError as e:
        print(f"Error: Missing required file: {e.filename}")
        print("Please ensure features.csv and your manual labels.csv are present.")
        return

    # Merge features with labels based on file and line number
    # This ensures each flow gets its correct "safe" or "tainted" label
    data_df = pd.merge(features_df, labels_df, on=['filename', 'sink_lineno'])

    if data_df.empty:
        print("Error: No matching data found between features and labels. Please check your CSV files.")
        return

    print(f"[*] Found {len(data_df)} labeled flows for training.")

    # Define features (X) and target (y)
    X = data_df.drop(columns=['label', 'filename', 'sink_lineno'])
    y = data_df['label']

    # Handle categorical features like 'sink_function' using one-hot encoding
    categorical_cols = ['sink_function']
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    X_encoded = pd.DataFrame(encoder.fit_transform(X[categorical_cols]))
    X_encoded.columns = encoder.get_feature_names_out(categorical_cols)
    
    # Drop original categorical columns and concatenate encoded ones
    X_processed = X.drop(columns=categorical_cols).reset_index(drop=True)
    X_final = pd.concat([X_processed, X_encoded], axis=1)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_final, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print("[*] Training the Decision Tree model...")
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model and the encoder
    joblib.dump({'model': model, 'encoder': encoder}, model_output_path)
    print(f"✅ Model and encoder saved to '{model_output_path}'")

    # Evaluate the model
    print("\n--- Model Evaluation ---")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy on Test Set: {accuracy:.2f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()