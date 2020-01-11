import os
import time
from tweepy import OAuthHandler, API, Stream, StreamListener
from BotStreamListener import BotStreamListener
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    listener = BotStreamListener(api=api)

    stream = Stream(auth, listener)
    stream.filter(track=["@bjnfess"])

    while True:
        api.list_direct_messages()

        time.sleep(60 * 1000)
