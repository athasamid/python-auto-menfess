from tweepy import StreamListener, API, TweepError
from ImageQuotes import ImageQuotes


class BotStreamListener(StreamListener):

    def __init__(self, api: API, db):
        self.api = api
        self.db = db
        self.user_model = db.users
        self.status_model = db.status
        self.quotes = db.quotes

    def process_data(self, twitter):
        print(twitter)
        self.save_user(twitter.user)
        if any(hashtag['text'] == 'rt' for hashtag in twitter.entities['hashtags']) and twitter.retweeted == False:
            print("found rts")
            if twitter.in_reply_to_status_id is not None:
                self.do_retweet(twitter.in_reply_to_status_id)

            else:
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
            updated_status = self.api.update_status(media_ids=[media.media_id], in_reply_to_status_id=in_reply_to_status_id,
                                   auto_populate_reply_metadata=True)
            self.status_model.insert_one(updated_status._json)
        except TweepError:
            print("error")

    def save_user(self, user):
        useravailable = self.user_model.find_one({'id': user.id})
        if useravailable is None:
            self.user_model.insert_one(user._json)

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
            retweeted = self.api.retweet(id=id)
            self.status_model.insert_one(retweeted._json)
        except TweepError:
            print("error ")

    def tweet(self, status):
        try:
            updated_status = self.api.update_status(status=status)
            self.status_model.insert_one(updated_status._json)
        except TweepError:
            print("error")

    def on_status(self, status):
        self.process_data(status)
        return True

    def on_error(self, status_code):
        print(status_code)

    def save_status(self, status):
        self.status_model.insert_one(self.set_status(status, None))

    def set_status(self, status, id_dm):
        return {
            'id': status.id,
            'id_dm': id_dm,
            'created_at': status.created_at,
            'text': status.text,
            'entities': status.entities,
            'in_reply_to_status_id': status.in_reply_to_status_id
        }
