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
    'access_token_secret': os.getenv("ACCESS_TOKEN_SECRET")
}

if __name__ == '__main__':
    auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = API(auth)
    client = MongoClient(os.getenv("MONGO_HOST"))

    db = client[os.getenv("MONGO_DB")]

    # response = auth.oauth.request('GET', "https://api.twitter.com/1.1/statuses/home_timeline.json")
    # print(response.headers)
    # print(response.content)
    # print(response.status_code)
    # with open('imgdm/743563732375113732.jpg', 'wb') as out_file:
    #     out_file.write(response.content)

    # media = self.api.media_upload(filename='imgdm/743563732375113732.jpg')

    while True:
        msg = api.list_direct_messages()
        print(msg)
        dmlistener = DMListener(api, msg, db, os.getenv("TRIGGER"), keys)
        dmlistener.process_dm()
        time.sleep(60 * 5)
