from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# --- TOKENIZER: Converts text to numbers ---
# Why? Models don't understand text, they understand numbers
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
# "distilbert-base-uncased": Smaller, faster version of BERT
# "uncased": Ignores case (the vs THE both → "the")

# --- MODEL: Pre-trained for text classification ---
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english",
    num_labels=2  # 2 labels: positive/negative
)

# --- STEP 1: Tokenize the input ---
text = "MCP server is requesting unusual file access patterns."
tokens = tokenizer(
    text,
    padding=True,      # Make all sequences same length
    truncation=True,   # Cut off long sequences
    return_tensors="pt"  # Return PyTorch tensors
)

print("Tokens:", tokens)
# Output: {'input_ids': tensor([[...]]), 'attention_mask': tensor([[...]])}
# input_ids: numbers representing each word
# attention_mask: tells model which tokens are actual words (not padding)

# --- STEP 2: Get predictions ---
with torch.no_grad():  # Disable gradient tracking (faster, less memory)
    outputs = model(**tokens)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)

print(f"Confidence: {probabilities[0][1]:.2f}")
# If output is 0.95, model is 95% confident this is negative/unsafe
# If output is 0.05, model is 95% confident this is positive/safe

# --- USING THE PIPELINE (EASIER WAY) ---
# Pipeline handles tokenization + model inference for you
from transformers import pipeline

classifier = pipeline("text-classification",
                     model="distilbert-base-uncased-finetuned-sst-2-english")

result = classifier("MCP server is functioning normally.")
print(result)
# [{'label': 'POSITIVE', 'score': 0.99}]
# POSITIVE means the model thinks this is safe/normal behavior & NEGATIVE means unsafe/anomalous behavior