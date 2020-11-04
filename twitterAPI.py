#!/usr/bin/env python
# manual filter attempt for parsing the twitter data. 
# from __future__ import absolute_import, print_function


from tweepy.streaming import StreamListener
import tweepy
import credentials as creds
import OSCConnector as osc
import NLPHandler as nlp
import time


auth = tweepy.OAuthHandler(creds.CONSUMER_KEY, creds.CONSUMER_SECRET)
auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)




# --------------------------------------------------------------
# 4. Define your functions


def home_timeline():
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)


def get_tweets(word, n, write=True):
    # initialize a list to hold all the tweepy Tweets
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=word, tweet_mode='extended').items(n):
        en_lang = tweet.metadata['iso_language_code'] == "en"
        tweet_text = tweet.full_text.lower().replace("\n", " ") + "\n"
        if (not tweet.retweeted) and ('rt @' not in tweet_text) and en_lang:
            print(tweet_text)
            if write:
                with open(path_address, 'a') as file:
                    try:
                        file.write(tweet_text)
                    except:
                        print("Exception Occurred")
                return
            else:
                return tweets


class StdOutListener(StreamListener):
    def on_status(self, tweet):
        try:
            tweet_text = tweet.text.lower().replace("\n", " ") + "\n"
            if (not tweet.retweeted) and ('rt @' not in tweet_text):
                try:
                    tweet_text = tweet.extended_tweet['full_text'].lower().replace("\n", " ") + "\n"
                finally:
                    time.sleep(5)
                    for phrase in nlp.get_noun_phrases(tweet_text):
                        osc.send(phrase)
        except:
            pass

    def on_error(self, error):
        print(error)
        return True  # tocontinue listening


def track(word: str):
    listener = StdOutListener()
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=[word], languages=["en"])
    time.sleep(5)
    stream.disconnect()
    return


track("#Election2020")
