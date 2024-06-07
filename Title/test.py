# !pip install langdetect
# !pip install nltk
# !pip install --no-cache-dir transformers sentencepiece
from langdetect import detect
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# Download NLTK data (you only need to do this once)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
model_name = "theblackcat102/alpaca-title-generator-mt0-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
def title_genration(input):
    # Load the pre-trained model and tokenizer

    # Encode the input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    # Generate a title
    output = model.generate(input_ids, max_length=30, repetition_penalty=1.2, top_k=50, num_return_sequences=1, early_stopping=True)
    # Decode and print the generated title
    generated_title = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_title
def extract_adj_noun(text):
    # Tokenize the text
    words = word_tokenize(text)
    # Perform part-of-speech tagging
    tagged_words = pos_tag(words)
    # Extract Adjectives and Nouns
    adj_noun_list = [word for word, tag in tagged_words if tag in ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS']]
    return adj_noun_list
input_text = """
The law is not meant to act a trap,” was a crucial statement, and a long-awaited reprieve, recently given by the Islamabad High Court (IHC) not only to Rahil Azizi — an Afghan refugee woman living in Pakistan — but also to the thousands of Afghan refugees living precarious lives in the country. Rahil Azizi vs. The State & others. can be considered a milestone in Pakistan’s judicial engagement with the 1951 Refugee Convention, despite the fact that Pakistan has not ratified the Convention or its 1967 Protocol.
For the first time in Pakistan’s judicial history, Article 31 of the 1951 Refugee Convention, which deals with the situation of refugees unlawfully in the country of refuge, is referenced in full and the provision’s application is linked with the domestic law, The Foreigners Act 1946, which hitherto governed the cases related to Afghan refugees and asylum seekers. Given the caretaker government’s recent decision to deport Afghans by November 1, 2023, this judgment must be viewed as a promising development of law and therefore needs careful attention. It can work as a timely aid to hundreds of Afghan refugees who are being subjected to arbitrary arrests, detentions, trials and deportation to Afghanistan in large numbers since November 2022 across Pakistan, after being charged with illegal entry and stay. The Pakistan government recently decided to expel all illegal migrants from the country. However, such policies fail to take into account the legal, political and administrative issues that have kept Afghan refugees in a perpetual state of stasis. The precarity experienced by Afghans seeking refuge in Pakistan has risen alarmingly in the last year, with many of them having to hide for fear of arrest by the police and, consequently, many are battling poverty since they have lost their daily wage jobs.
"""
uncleaned_title = title_genration(input_text)
# Call the function and get the list of Adjectives and Nouns
result = extract_adj_noun(uncleaned_title)
result_string = ' '.join(result)
# Print the result
print(result_string)