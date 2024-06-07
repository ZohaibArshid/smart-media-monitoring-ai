import transformers
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# Define a function to summarize Urdu text into a title
# Load the pre-trained model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
def summarize_text(input_text):
    print("english summary generation on progress")
    # Encode the input text
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    # Generate a title
    output = model.generate(input_ids, max_length=300, repetition_penalty=1.2, top_k=50, num_return_sequences=1, early_stopping=True)
    # Decode and print the generated title
    generated_summry = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_summry
# input_text = """
# South DIG Syed Asad Raza told Dawn.com that unidentified individuals on a motorcycle threw a hand grenade outside a shop that had been closed for months before fleeing the scene.
# The authorities are investigating the motive behind the attack, the police official said before adding that it appeared to be a random act without a specific target.
# The DIG said that seven people sustained injuries, while one of them — a 35-year-old named Razia Mohammed Ali — was in critical condition before succumbing to her wounds.
# He said all of the injured were bystanders and had been transported to Dr Ruth Pfau Civil Hospital in Karachi. They were identified as Zohaib Javed, Khairullah, Wansh Dileep Kumar, Ateeqa Adam, Adil Adam and Ahsan Nabi.
# """
# summry = summarize_text(input_text)
# print(summry)