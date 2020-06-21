import os
import time
from tweepy import OAuthHandler, API, Stream, StreamListener
from BotStreamListener import BotStreamListener
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth, wait_on_rate_limit=True)

    client = MongoClient(os.getenv("MONGO_HOST"))

    db = client[os.getenv("MONGO_DB")]
    listener = BotStreamListener(api=api, db=db)

    stream = Stream(auth, listener, verify=False)
    stream.filter(track=[os.getenv("USERNAME")])
