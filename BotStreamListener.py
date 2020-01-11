from tweepy import StreamListener, API, TweepError
from models.Twitter import Twitter
from ImageQuotes import ImageQuotes
import jsonpickle
from elasticsearch import Elasticsearch

# from firebase import firebase

es = Elasticsearch()


class BotStreamListener(StreamListener):

    def __init__(self, api: API):
        self.api = api
        # self.firebase = firebase

    def process_data(self, twitter):
        if any(hashtag['text'] == 'rt' for hashtag in twitter.entities['hashtags']) and twitter.retweeted == False:
            print("found rts")
            if twitter.in_reply_to_status_id is not None:
                self.do_retweet(twitter.in_reply_to_status_id)
            else:
                print()
                self.do_retweet(id=twitter.id)

        if any(hashtag['text'] == 'quoteimg' for hashtag in twitter.entities['hashtags']):
            print("found quoteimg")
            in_reply_to_status_id = twitter.id
            twit_to_quotes = twitter
            if twitter.in_reply_to_status_id is not None:
                twit_to_quotes = self.get_tweet(id=twitter.in_reply_to_status_id)

            self.do_quotes(data=twit_to_quotes, in_reply_to_status_id=in_reply_to_status_id)

    def do_quotes(self, data, in_reply_to_status_id):
        try:
            me = self.get_me()
            image_quotes = ImageQuotes(data, username='@' + me.screen_name)
            image_quotes.makeImage()
            media = self.api.media_upload(filename='quotes/' + data.id_str + '.jpg')
            print(media)
            print(in_reply_to_status_id)
            self.api.update_status(media_ids=[media.media_id], in_reply_to_status_id=in_reply_to_status_id,
                                   auto_populate_reply_metadata=True)
        except TweepError:
            print("error")

    def get_me(self):
        try:
            return self.api.me()
        except TweepError:
            print("error")

    def get_tweet(self, id: int):
        try:
            return self.api.get_status(id=id)
        except TweepError:
            print("error")

    def do_retweet(self, id: int):
        try:
            self.api.retweet(id=id)
        except TweepError:
            print("error ")

    def tweet(self, status):
        try:
            self.api.update_status(status=status)
        except TweepError:
            print("error")

    def on_status(self, status):
        self.process_data(status)
        return True

    def on_error(self, status_code):
        print(status_code)
