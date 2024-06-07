from transformers import pipeline
model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
def sentiment_analysis(text):
    print("sentiment_analysis generation on progress")
    result=sentiment_task(text)
    label = result[0]['label']
    return label