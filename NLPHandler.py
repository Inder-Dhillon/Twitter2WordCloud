from textblob import TextBlob


def get_noun_phrases(text):
    return TextBlob(text).noun_phrases


def get_sentiment(text):
    return TextBlob(text).sentiment
