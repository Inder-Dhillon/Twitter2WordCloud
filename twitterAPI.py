#!/usr/bin/env python
# manual filter attempt for parsing the twitter data. 
# from __future__ import absolute_import, print_function


from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy
import os
import credentials as creds

# SETUP
# --------------------------------------------------------------

# 1. Authenticate the Tweepy API

auth = tweepy.OAuthHandler(creds.CONSUMER_KEY, creds.CONSUMER_SECRET)
auth.set_access_token(creds.ACCESS_TOKEN, creds.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# get save path (pwd in command line)
save_path = os.getcwd()  # current working directory
name_of_file = 'results.txt'
path_address = os.path.join(save_path, name_of_file)
# print path_address
file_exists = os.path.isfile(path_address)


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
    def on_status(self, status):
        try:
            with open(path_address, 'a') as file:
                if (not status.retweeted) and ('RT @' not in status.text):
                    tweet_text = status.text
                    file.write(tweet_text + '\n')
                    print(tweet_text)
        except:
            pass

    def on_error(self, error):
        print(error)
        return True  # tocontinue listening


def track(word: str):
    listener = StdOutListener()
    stream = Stream(auth, listener)
    stream.filter(track=[word], languages=["en"], )
    stream.filter()
    stream.disconnect()
    return


# track("#Election2020")
get_tweets("#Election2020", 1000)
