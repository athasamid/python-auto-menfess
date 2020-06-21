import os
import time
from tweepy import OAuthHandler, API, Stream, StreamListener, AppAuthHandler
from DMListener import DMListener
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

keys = {
    'consumer_key': os.getenv("CONSUMER_KEY"),
    'consumer_secret': os.getenv("CONSUMER_SECRET"),
    'access_token': os.getenv("ACCESS_TOKEN"),
    'access_token_secret': os.getenv("ACCESS_TOKEN_SECRET"),
    'username': os.getenv('USERNAME'),
    'trigger': os.getenv("TRIGGER")
}

if __name__ == '__main__':
    auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = API(auth)
    client = MongoClient(os.getenv("MONGO_HOST"))

    db = client[os.getenv("MONGO_DB")]

    while True:
        print("Check dm")
        msg = api.list_direct_messages()
        dmlistener = DMListener(api, msg, db, os.getenv("TRIGGER"), keys)
        dmlistener.process_dm()
        time.sleep(60 * 5)
