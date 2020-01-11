from tweepy import StreamListener, API, TweepError
from models.Twitter import Twitter
import jsonpickle
from elasticsearch import Elasticsearch

es = Elasticsearch()


class BotStreamListener(StreamListener):

    def __init__(self, api: API):
        self.api = api

    def process_data(self, twitter):
        print(twitter)
        if filter(lambda x: x.text == 'bjnfessrt', twitter['entities']['hashtags']):
            print("found rts")
            if twitter['in_reply_to_status_id'] is not None:
                self.do_retweet(twitter['in_reply_to_status_id'])
            else:
                print()
                self.do_retweet(id=twitter['id'])
        elif filter(lambda x: x.text == 'bjnfessquoteimg', twitter['entities']['hashtags']):
            print("found quoteimg")
            # if twitter['in_reply_to_status_id'] is not None:
            #     self.do_quotes(twitter)
            # else:
            #     print()
            #     self.do_quotes(id=twitter['id'])

    # def do_quotes(self, data):
    #     try:
    #         self.api.media_upload()

    def do_retweet(self, id: int):
        try:
            self.api.retweet(id = id)
        except TweepError:
            print("error ")

    def tweet(self, status):
        try:
            self.api.update_status(status=status)
        except TweepError:
            print("error")

    def on_data(self, raw_data):
        twitter = jsonpickle.decode(raw_data, classes=Twitter)
        self.process_data(twitter)
        return True

    def on_error(self, status_code):
        print(status_code)
