from tweepy import StreamListener, API, TweepError
from requests_oauthlib import OAuth1Session
from PIL import Image, ImageFont, ImageDraw
import requests


class DMListener(object):
    def __init__(self, api: API, dms, db, trigger, keys):
        self.api = api
        self.dms = dms
        self.trigger = trigger
        self.db = db
        self.keys = keys
        self.dbdm = db.directmessage

    def process_dm(self):
        for dm in self.dms:
            getdm = self.dbdm.find_one({'id': dm.id})
            if getdm is None:
                print("Inserting new Data")
                self.dbdm.insert_one(self.set_dms(dm))
                self.check_tweet(dm)

    def check_tweet(self, dm):
        print(self.trigger)
        if dm.message_create['message_data']['text'].lower().startswith(self.trigger.lower()):
            status = dm.message_create['message_data']['text']
            urls = dm.message_create['message_data']['entities']['urls']

            id_media = None

            try:
                media_url = dm.message_create['message_data']['attachment']['media']['media_url']
                dm_id = dm.id
                media_type = dm.message_create['message_data']['attachment']['media']['type']
                if media_type == 'photo':
                    id_media = [self.download_and_upload_media(media_url, dm_id)]
            except KeyError:
                print('key_error')

            print(id_media)

            url = None
            for i in urls:
                if 'twitter.com' in i['expanded_url']:
                    status.replace(i['url'], '')
                    url = i['expanded_url'] if (
                                dm.message_create['message_data']['attachment']['media']['url'] != i['url']) else None

            self.api.update_status(status=status, attachment_url=url, media_ids=id_media)

    def download_and_upload_media(self, url, dm_id):
        tw = OAuth1Session(self.keys['consumer_key'], self.keys['consumer_secret'], self.keys['access_token'], self.keys['access_token_secret'])
        response = tw.get(url, stream=True, allow_redirects=False)
        if response.status_code == 200:
            with open('imgdm/' + dm_id + '.jpg', 'wb') as out_file:
                out_file.write(response.content)

            media = self.api.media_upload(filename='imgdm/' + dm_id + '.jpg')

            return media.media_id

        return None

    def set_dms(self, dm):
        return {
            'id': dm.id,
            'created_timestamp': dm.created_timestamp,
            'type': dm.type,
            'message_create': dm.message_create
        }
