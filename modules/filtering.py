import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import string
import re

def filter_tweet(tweet):

    stop_words = set(stopwords.words('english'))        #eliminate stopwords

    emoji_sequence = re.compile("["
        u"\U0001F600-\U0001F64F" 
        u"\U0001F300-\U0001F5FF" 
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF" 
                           "]+", flags=re.UNICODE)

    tweet = emoji_sequence.sub(r'', tweet)
    words = tweet.split()

    stopwords_eliminated = [w for w in words if not w.lower() in stop_words]
    
    filtered_sentence = []
    
    for w in stopwords_eliminated:      #this way the result is lowercase, without punctuation
        if w not in stop_words:
            filtered_sentence.append(w.lower().translate(str.maketrans('', '', string.punctuation)))

    result = " ".join(filtered_sentence)

    return result
