from models.Hashtag import Hashtag
from models.Media import Media
from models.Url import Url
from models.UserMention import UserMention
from models.Symbol import Symbol


class Entities(object):
    def __init__(self, hashtags: [Hashtag], media: [Media], urls: [Url], user_mentions: [UserMention],
                 symbols: [Symbol]):
        self.hashtags = hashtags
        self.media = media
        self.urls = urls
        self.user_mentions = user_mentions
        self.symbols = symbols
