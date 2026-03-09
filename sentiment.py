import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load the FinBERT sentiment analysis pipeline
# The model 'ProsusAI/finbert' is the standard pre-trained version
classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert")

# Example financial sentences
sentences = [
    "The company's revenue increased by 20% this quarter.",
    "Stock prices plummeted following the unexpected loss.",
    "The market outlook remains stable for the next fiscal year."
]

# Run inference
results = classifier(sentences)

for text, res in zip(sentences, results):
    print(f"Text: {text}\nResult: {res['label']} (Score: {res['score']:.4f})\n")