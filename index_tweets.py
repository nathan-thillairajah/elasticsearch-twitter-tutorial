import sys
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch
from config import *

es = Elasticsearch()

class TweetStreamListener(StreamListener):
    def __init__(self, tweetFilter):
        self.tweetFilter = tweetFilter

    def on_data(self, data):
        dict_data = json.loads(data)
        tweet = TextBlob(dict_data["text"])

        print(dict_data["text"])

        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        print(sentiment)

        es.index(index="tweets",
                 doc_type="_doc",
                 body={"author": dict_data["user"]["screen_name"],
                       "date": dict_data["created_at"],
                       "message": dict_data["text"],
                       "polarity": tweet.sentiment.polarity,
                       "subjectivity": tweet.sentiment.subjectivity,
                       "sentiment": sentiment,
                       "filter": self.tweetFilter})
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    tweetFilter = 'final four'
    if len(sys.argv) == 2:
        tweetFilter = sys.argv[1]

    listener = TweetStreamListener(tweetFilter)

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track=[tweetFilter])