import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# # Load the model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained("google/muril-base-cased")
# model = AutoModelForSequenceClassification.from_pretrained("MichaelHuang/muril_base_cased_urdu_sentiment")
# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("google/muril-base-cased")
model = AutoModelForSequenceClassification.from_pretrained("MichaelHuang/muril_base_cased_urdu_sentiment_2.0")



# Define the input text
text = '''
لیکن مسٹر پوتن نے یہ بھی کہا کہ یہ منصوبہ اسی وقت پیش کیا جا سکتا ہے جب لوگ 'مغرب اور کیئو میں' اس کے لیے تیار ہوں۔
روسی رہنما نے منگل کو ماسکو میں چینی صدر شی جن پنگ سے ملاقات کی جس میں روس یوکرین جنگ اور دونوں ممالک کے درمیان تعلقات پر تبادلہ خیال کیا گیا۔
گذشتہ ماہ شائع ہونے والے چین کے منصوبے میں واضح طور پر روس سے یوکرین چھوڑنے کا مطالبہ نہیں کیا گیا ہے۔
'''

# Tokenize the input text
inputs = tokenizer(text, return_tensors='pt')

# Make a prediction
outputs = model(**inputs)
predicted_class = torch.argmax(outputs.logits).item()

# Print the predicted class
if predicted_class == 1:
    print('Positive')
else:
    print('Negative')
