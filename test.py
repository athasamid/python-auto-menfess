from tweepy import OAuthHandler, API, Stream, StreamListener
from dotenv import load_dotenv
import os
import glob
from ImageQuotes import ImageQuotes

load_dotenv()

from pymongo import MongoClient

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth, wait_on_rate_limit=True)

client = MongoClient(os.getenv("MONGO_HOST"))
db = client[os.getenv("MONGO_DB")]

# status = api.get_direct_message(id=1274766998874931204)
# print(status)

status = api.get_status(id=1274694009395376129)
me = api.me()
print(status)
print(me)
image_quotes = ImageQuotes(status, username='@' + me.screen_name)
image_quotes.makeImage()

# if db.users.count_documents({'id': me.id}, limit=1) == 0:
#     print("saving user "+me.id_str)
#     db.users.insert_one(me._json)