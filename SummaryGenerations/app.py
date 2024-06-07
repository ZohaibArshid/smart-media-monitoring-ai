
# !pip install --no-cache-dir transformers sentencepiece
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
import concurrent.futures
import asyncio
app = FastAPI()
WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
def translate_urdu_to_english(urdu_text):
    try:
        english_translation = translate(urdu_text, "en", "ur")
        return english_translation
    except Exception as e:
        return str(e)
def summarize(text: str):
    input_ids = tokenizer(
    [WHITESPACE_HANDLER(text)],return_tensors="pt",padding="max_length",truncation=True,max_length=512)["input_ids"]
    output_ids = model.generate(
        input_ids=input_ids,
        max_length=300,
        no_repeat_ngram_size=2,
        num_beams=1
    )[0]
    summary = tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )
    
    return {"urdu_summary":summary,"english_summary":translate_urdu_to_english(summary)}

user_api_keys = {
    "user1": "apikey1",
    "user2": "apikey2",
    # Add more users and their API keys as needed
}



# Dependency to validate the API key
async def get_api_key(api_key: str = Header(None, convert_underscores=False)):
    if api_key not in user_api_keys.values():
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key
@app.post("/SummaryGeneration")
async def SummaryGeneration_endpoint(
    text: str,
    api_key: str = Depends(get_api_key),  # Require API key for this route
):
    # Create a new thread for processing each user's video
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: summarize(text)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1002,reload=True)
    
# run command in cmd 
# uvicorn app:app --host 0.0.0.0 --port 1002 --reload


# article_text = """
# پاکستان سے تعلق رکھنے والے سوشل میڈیا سلیبریٹیز ڈکی بھائی اور مومن ثاقب نے اِس خبر کی تردید کی ہے کہ اُن کے انڈیا کے ویزے مسترد ہو گئے ہیں۔
# سوشل میڈیا پر گزشتہ کچھ دنوں سے افواہیں گردش کر رہی تھیں کہ
#  ڈکی بھائی (سعد الرحمان) اور مومن ثاقب کے ورلڈ کپ کے لیے انڈیا کے ویزے مسترد ہو گئے ہیں جس کے بعد دونوں سوشل میڈیا ستاروں نے اس بات کی وضاحت کر دی ہے۔"""
