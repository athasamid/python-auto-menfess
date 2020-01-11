class SizeObject(object):
    def __init__(self, h, resize, w):
        self.h = h
        self.resize = resize
        self.w = w


class Sizes(object):
    def __init__(self, thumb: SizeObject, large: SizeObject, medium: SizeObject, small: SizeObject):
        self.thumb = thumb
        self.large = large
        self.medium = medium
        self.small = small


class Size(object):
    def __init__(self, sizes: Sizes):
        self.sizes = sizes


class Media(object):
    def __init__(self, display_url, expanded_url, id, id_str, media_url, media_url_https, source_status_id, source_status_id_str, type, url):
        self.display_url = display_url
        self.expanded_url = expanded_url
        self.id = id
        self.id_srt = id_str
        self.media_url = media_url
        self.media_url_https = media_url_https
        self.source_status_id = source_status_id
        self.source_status_id_str = source_status_id_str
        self.type = type
        self.url = url
