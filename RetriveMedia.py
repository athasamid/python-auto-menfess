import random
import string
import time
import urllib
import urllib3
import codecs
import requests
import binascii
from urllib.parse import urlparse
import hmac
from requests_oauthlib import OAuth1Session
import hashlib


def escape(s):
    """Escape a URL including any /."""
    return urllib.parse.quote(s, safe='~')


def _utf8_str(s):
    """Convert unicode to utf-8."""
    try:
        return s.encode("utf-8")
    except:
        return str(s)


class RetriveMedia:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def timestamp(self):
        return int(round(time.time()))

    def generateNonce(self):
        nonce = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(32))

        return nonce

    def get_normalized_url(self, url):
        parts = urlparse(url)
        scheme, netloc, path = parts[:3]
        # Exclude default port numbers.
        if scheme == 'http' and netloc[-3:] == ':80':
            netloc = netloc[:-3]
        elif scheme == 'https' and netloc[-4:] == ':443':
            netloc = netloc[:-4]
        return '%s://%s%s' % (scheme, netloc, path)

    def get_normalized_param(self, params):
        try:
            del params['oauth_signature']
        except KeyError:
            pass

        key_values = [(escape(_utf8_str(k)), escape(_utf8_str(v))) for k, v in params.items()]
        key_values.sort()

        return '&'.join(['%s=%s' % (k, v) for k, v in key_values])

    def signatureBaseForRequest(self, url, params, method):

        sig = (
            escape(method.upper()),
            escape(self.get_normalized_url(url)),
            escape(self.get_normalized_param(params))
        )

        key = escape(self.consumer_key) + '&' + escape(self.access_token_secret)
        raw = escape('&').join(sig)
        print(key)
        print(raw)
        return key, raw

    def signingKey(self):
        return self.consumer_secret + self.access_token_secret

    def signSignature(self, signature_base):
        key, raw = signature_base

        try:
            import hashlib
            hashed = hmac.new(key.encode("utf-8"), raw.encode("utf-8"), hashlib.sha1)
        except ImportError:
            import sha
            hashed = hmac.new(key.encode("utf-8"), raw.encode("utf-8"), sha)

        return binascii.b2a_base64(hashed.digest())[:-1].decode('utf-8')

    def signatureForRequest(self, url, params, method):
        signature_base = self.signatureBaseForRequest(url, params, method)

        signature = self.signSignature(signature_base)

        return signature

    def headerDictionaryWithoutSignature(self):
        headers = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': self.generateNonce(),
            'oauth_signature_method': "HMAC-SHA1",
            'oauth_timestamp': str(self.timestamp()),
            'oauth_token': self.access_token,
            'oauth_version': "1.0"
        }
        return headers

    def headerStringForRequest(self, url, params, method):
        headers = self.headerDictionaryWithoutSignature()

        for key, value in headers.items():
            params[key] = value

        headers['oauth_signature'] = self.signatureForRequest(url, params, method)
        headers_keys = sorted(headers)

        header_string = "OAuth "

        for key in headers_keys:
            value = headers[key]

            hstring = urllib.parse.quote_plus(key) + "=\"" + urllib.parse.quote_plus(value) + "\", "
            header_string += hstring

        header_string = header_string[:-2]
        return header_string

    def getMedia(self, media_url, **kwargs):
        auth_header = self.headerStringForRequest(media_url, {}, "GET")
        print(auth_header)
        request = requests.get(media_url, headers={"authorization ": auth_header}, **kwargs)
        return request


if __name__ == "__main__":
    twm = OAuth1Session("NEkIYTmF9gI9U2PApw8RzCkRt", "oeOaTuIhcrWolFBcRrfsoTOqvlX8X1jiSEjcHz0HsS84zdJLLK",
                                 "483456845-3t1BQUvNb6qfHR4pMMGSvKeax0u0mLWlS6nqfUaW",
                                 "3bMwXsvJaxcBA30i0yTwAkii3srQNxBFjcbkN8Db21Hyd")
    try:
        response = twm.get(
            "https://ton.twitter.com/1.1/ton/data/dm/1216424434682089476/1216424428529045504/XzmiUIj_.jpg:medium",
            stream=True,
            allow_redirects=False)
        print(response.status_code)
        print(response.raw.reason)
        print(response.headers)
        with open('imgdm/743563732375113732.jpg', 'wb') as out_file:
            out_file.write(response.raw)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
