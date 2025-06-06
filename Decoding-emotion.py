# Upload the Dataset (if not already uploaded in your environment)
# from google.colab import files
# uploaded = files.upload()

# Load the Dataset
import pandas as pd

# Load the data
df = pd.read_csv('/content/Tweets.csv')

# Data Exploration
print("First 5 Rows:")
print(df.head())

print("\nShape of the dataset:", df.shape)
print("\nColumns:", df.columns.tolist())

print("\nInfo:")
print(df.info())

print("\nSummary statistics:")
print(df.describe(include='all'))

# Check for Missing Values and Duplicates
print("\nMissing values per column:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

# Basic Visualization (optional)
import seaborn as sns
import matplotlib.pyplot as plt

# Sentiment distribution
sns.countplot(data=df, x='airline_sentiment')
plt.title('Sentiment Distribution')
plt.show()

# Preprocessing for Sentiment Analysis

# We'll use only relevant columns
df_model = df[['text', 'airline_sentiment']].dropna()

# Encode target
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df_model['sentiment_encoded'] = le.fit_transform(df_model['airline_sentiment'])

# Text preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(df_model['text'])
y = df_model['sentiment_encoded']

# Train-Test Split and Model Training
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))

# Gradio Interface for Sentiment Prediction
!pip install gradio

import gradio as gr

def predict_sentiment(text):
    vectorized_text = vectorizer.transform([text])
    prediction = model.predict(vectorized_text)[0]
    return le.inverse_transform([prediction])[0]

gr.Interface(
    fn=predict_sentiment,
    inputs=gr.Textbox(lines=4, label="Tweet Text"),
    outputs=gr.Label(label="Predicted Sentiment"),
    title="✈️ Airline Tweet Sentiment Predictor",
    description="Enter a tweet related to an airline to predict whether it's positive, negative, or neutral."
).launch()
