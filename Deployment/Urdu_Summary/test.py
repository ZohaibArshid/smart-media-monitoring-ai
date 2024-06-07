from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re 
WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
def summarize(text):
    print("urdu summary generation in progress")
    # print(text)
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
    return summary