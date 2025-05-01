import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import bigrams
from nltk.stem import PorterStemmer


def remove_stemmed_phrases(tokens, phrase_list):
    text = ' '.join(tokens)
    for phrase in phrase_list:
        text = re.sub(rf"\b{re.escape(phrase)}\b", "", text)
    return text.split()


def clean_and_stem(text):
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    custom_stop_phrases = [
        "angelica evan", "christina harward", "click read", "click see", "et click",
        "frederick kagan", "full report", "karolina hird", "isw assess", "isw continu",
        "isw cover", "isw interact", "isw observ", "isw previous", "kateryna stepanenko",
        "key takeaway", "map present", "map russian", "map updat", "nicol wolkov", "pm et",
        "present report", "previous assess", "previous report", "read full", "riley bailey",
        "see isw", "static map", "takeaway russian", "timelaps map"
    ]

    stemmed_custom_phrases = [
        ' '.join([stemmer.stem(word) for word in phrase.split()])
        for phrase in custom_stop_phrases
    ]

    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@\w+|\#', '', text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = text.lower()

    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    stemmed = [stemmer.stem(token) for token in tokens]
    cleaned_tokens = remove_stemmed_phrases(stemmed, stemmed_custom_phrases)

    return cleaned_tokens


def bigram_tokenizer(text):
    tokens = clean_and_stem(text)
    return [' '.join(bg) for bg in bigrams(tokens)]
