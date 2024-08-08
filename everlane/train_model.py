import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the dataset
data = pd.read_csv('testrec.csv')

# Preprocess the data
X = data[['skin_type', 'height', 'gender', 'season', 'usage']]
y = data['product_id']

# Convert categorical variables to numerical
X = pd.get_dummies(X)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Save the model
joblib.dump(clf, 'recommendation_model.pkl')
