import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

FEATURES_CSV = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis\deadcode\features.csv"
MODEL_PATH = r"C:\Users\lahar\OneDrive\Desktop\Python\TOAC\DeadCodeTaintAnalysis\deadcode\model.pkl"

df = pd.read_csv(FEATURES_CSV)
df = df[df["label"].isin(["used", "unused"])] 

X = df[["name_length", "is_class", "has_underscore"]]
X["is_class"] = X["is_class"].astype(int)
X["has_underscore"] = X["has_underscore"].astype(int)

y = LabelEncoder().fit_transform(df["label"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

joblib.dump(model, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")
