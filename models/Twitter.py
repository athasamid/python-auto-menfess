from models.User import User
from models.Entities import Entities
from models.MatchingRules import MatchingRules


class Twitter(object):
    def __init__(self, created_at, id, id_str, text, source, truncated: bool, in_reply_to_status_id,
                 in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str, in_reply_to_screen_name,
                 user: User, quoted_status_id, quoted_status_id_str, is_quote_status: bool, quote_count, reply_count,
                 retweet_count, favorite_count, entities: [Entities], favorited: bool, retweeted: bool,
                 possibly_sensitive: bool, filter_level, lang, matching_rules=None):
        if matching_rules is None:
            matching_rules = [MatchingRules]
        self.created_at = created_at
        self.id = id
        self.id_str = id_str
        self.text = text
        self.source = source
        self.truncated = truncated
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_status_id_str = in_reply_to_status_id_str
        self.in_reply_to_user_id = in_reply_to_user_id
        self.in_reply_to_user_id_str = in_reply_to_user_id_str
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.user = user
        self.quoted_status_id = quoted_status_id
        self.quoted_status_id_str = quoted_status_id_str
        self.is_quote_status = is_quote_status
        self.quote_count = quote_count
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.entities = entities
        self.favorited = favorited
        self.retweeted = retweeted
        self.possibly_sensitive = possibly_sensitive
        self.filter_level = filter_level
        self.lang = lang
        self.matching_rules = matching_rules
