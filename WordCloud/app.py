# !pip install stanza
import stanza
from wordcloud import WordCloud, STOPWORDS
from fastapi import FastAPI, UploadFile, Depends, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
import concurrent.futures
import asyncio
app = FastAPI()

# Initialize the Urdu pipeline
stanza.download("ur")  # Download the Urdu model (if not already downloaded)
nlp = stanza.Pipeline("ur", processors="tokenize,pos")

# Process the text and perform part-of-speech tagging
def word_cloud(text: str):
    doc = nlp(text)
    nouns = []
    # Extract and print the tagged text
    previous_pos = None  # Store the previous part-of-speech tag
    current_word = ''    # Store the current word being formed
    for sentence in doc.sentences:
        for word in sentence.words:
            current_pos = word.pos
            #if current_pos in {"NOUN", "PROPN"}:
            if current_pos in {"PROPN"}:
                if current_pos == previous_pos or (previous_pos is None and current_pos == "PROPN"):
                    current_word += ' ' + word.text  # Add a space between consecutive PROPN words
                else:
                    if current_word:
                        nouns.append(current_word.strip())  # Strip any leading/trailing spaces
                    current_word = word.text
            else:
                if current_word:
                    nouns.append(current_word.strip())  # Strip any leading/trailing spaces
                current_word = ''
            previous_pos = current_pos
    # Append the last word if it's not already added
    if current_word:
        nouns.append(current_word.strip())  # Strip any leading/trailing spaces

    urdu_words = ", ".join(nouns)
    # print("urdu_words \n\n", urdu_words, "\n\n")
    word_freq = {}
    for noun in nouns:
        if noun in word_freq:
            word_freq[noun] += 1
        else:
            word_freq[noun] = 1
    # Print the word frequencies
    # for word, freq in word_freq.items():
    #     print(f"{word}: {freq}")
    # return word_freq
    transformed_data = [{"text": key, "value": value} for key, value in word_freq.items()]
    return transformed_data
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
@app.post("/WordCloud/")
async def WordCloud_endpoint(
    text: str,
    api_key: str = Depends(get_api_key),  # Require API key for this route
):
    # Create a new thread for processing each user's video
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: word_cloud(text)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1001,reload=True)
    
# run command in cmd 
# uvicorn app:app --host 0.0.0.0 --port 1001 --reload
