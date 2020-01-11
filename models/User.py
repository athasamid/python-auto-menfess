class User(object):
    def __init__(self, id, id_str, name, screen_name, location, url, description, verified, followers_count,
                 friends_count, listed_count, favourites_count, statuses_count, created_at, utc_offset, time_zone,
                 geo_enabled, lang, contributors_enabled, is_translator, profile_background_color,
                 profile_background_image_url, profile_background_image_url_https, profile_background_tile,
                 profile_link_color, profile_sidebar_border_color, profile_sidebar_fill_color, profile_text_color,
                 profile_use_background_image, profile_image_url, profile_image_url_https, profile_banner_url,
                 default_profile, default_profile_image, following, follow_request_sent, notifications):
        self.id = id
        self.id_str = id_str
        self.name = name
        self.screen_name = screen_name
        self.location = location
        self.url = url
        self.description = description
        self.verified = verified
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.listed_count = listed_count
        self.favourites_count = favourites_count
        self.statuses_count = statuses_count
        self.created_at = created_at
        self.utc_offset = utc_offset
        self.time_zone = time_zone
        self.geo_enabled = geo_enabled
        self.lang = lang
        self.contributors_enabled = contributors_enabled
        self.is_translator = is_translator
        self.profile_background_color = profile_background_color
        self.profile_background_image_url = profile_background_image_url
        self.profile_background_image_url_https = profile_background_image_url_https
        self.profile_background_tile = profile_background_tile
        self.profile_link_color = profile_link_color
        self.profile_sidebar_border_color = profile_sidebar_border_color
        self.profile_sidebar_fill_color = profile_sidebar_fill_color
        self.profile_text_color = profile_text_color
        self.profile_use_background_image = profile_use_background_image
        self.profile_image_url = profile_image_url
        self.profile_image_url_https = profile_image_url_https
        self.profile_banner_url = profile_banner_url
        self.default_profile = default_profile
        self.default_profile_image = default_profile_image
        self.following = following
        self.follow_request_sent = follow_request_sent
        self.notifications = notifications
