from fastapi import FastAPI, UploadFile, Depends, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
import concurrent.futures
import asyncio

# from transformers import AutoModelForSequenceClassification
# from transformers import TFAutoModelForSequenceClassification
# from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
app = FastAPI()
# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

# MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"
# output_director=r"D:\Forbmax User Data\waqar sahi\smart-media-monitoring-ai\AI Models"
# tokenizer = AutoTokenizer.from_pretrained(MODEL,cache_dir=output_director)
# config = AutoConfig.from_pretrained(MODEL,cache_dir=output_director)
# MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"

# tokenizer = AutoTokenizer.from_pretrained(MODEL)
# config = AutoConfig.from_pretrained(MODEL)

# # PT
# model = AutoModelForSequenceClassification.from_pretrained(MODEL)
user_api_keys = {
    "user1": "apikey1",
    "user2": "apikey2",
    # Add more users and their API keys as needed
}
from transformers import pipeline
model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
# sentiment_task("T'estimo!")

def analyze_sentiment(text: str):
    try:
        result = sentiment_task(text)
        label = result[0]['label']
        return label
        # text = preprocess(text)
        # encoded_input = tokenizer(text, return_tensors='pt')
        # output = model(**encoded_input)
        # scores = output[0][0].detach().numpy()
        # scores = softmax(scores)
        # top_class_idx = np.argmax(scores)
        # top_class = config.id2label[top_class_idx]
        # return top_class
        # ranking = np.argsort(scores)
        # ranking = ranking[::-1]
        # sentiment_scores={}
        # # print(ranking)
        # for i in range(scores.shape[0]):
        #     l = config.id2label[ranking[i]]
        #     s = scores[ranking[i]]
        #     sentiment_scores[l]=np.round(float(s), 4)
        # return sentiment_scores
    except Exception as e:
        return {"error": str(e)}

# Dependency to validate the API key
async def get_api_key(api_key: str = Header(None, convert_underscores=False)):
    if api_key not in user_api_keys.values():
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key
@app.post("/sentiment/")
async def sentiment_endpoint(
    text: str,
    api_key: str = Depends(get_api_key),  # Require API key for this route
):
    # Create a new thread for processing each user's video
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: analyze_sentiment(text)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1004,reload=True)
    
# run command in cmd 
# uvicorn app:app --host 0.0.0.0 --port 1004 --reload
