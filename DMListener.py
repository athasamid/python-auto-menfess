from requests_oauthlib import OAuth1Session
from tweepy import API
import os


class DMListener(object):
    def __init__(self, api: API, dms, db, trigger, keys):
        self.api = api
        self.dms = dms
        self.trigger = trigger
        self.db = db
        self.keys = keys
        self.dbdm = db.directmessage
        self.user_model = db.users
        self.status_model = db.statuses

    def process_dm(self):
        for dm in self.dms:
            getdm = self.dbdm.find_one({'id': dm.id})
            if getdm is None:
                self.save_user(dm.message_create["sender_id"])
                self.dbdm.insert_one(self.set_dms(dm))
                self.check_tweet(dm)
                print(dm)

    def check_tweet(self, dm):
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

            url = None
            for i in urls:
                if 'twitter.com' in i['expanded_url']:
                    status.replace(i['url'], '')
                    url = i['expanded_url'] if (
                                dm.message_create['message_data']['attachment']['media']['url'] != i['url']) else None

            updated_status = self.api.update_status(status=status, attachment_url=url, media_ids=id_media)
            self.status_model.insert_one(self.set_status(updated_status, dm.id))
            self.api.send_direct_message(recipient_id=dm.message_create['sender_id'], text="Request anda telah di terbitkan.\nSilahkan cek disini: https://twitter.com/"+self.keys['username'].replace('@', '')+"/status/"+updated_status.id_str)

    def download_and_upload_media(self, url, dm_id):
        tw = OAuth1Session(self.keys['consumer_key'], self.keys['consumer_secret'], self.keys['access_token'], self.keys['access_token_secret'])
        response = tw.get(url, stream=True, allow_redirects=False)
        if response.status_code == 200:
            dir_path = os.path.dirname(__file__)
            with open(dir_path+'/imgdm/' + dm_id + '.jpg', 'wb') as out_file:
                out_file.write(response.content)

            media = self.api.media_upload(filename=dir_path+'/imgdm/' + dm_id + '.jpg')

            return media.media_id

        return None

    def set_dms(self, dm):
        return {
            'id': dm.id,
            'created_timestamp': dm.created_timestamp,
            'type': dm.type,
            'message_create': dm.message_create
        }

    def set_status(self, status, id_dm):
        return {
            'id': status.id,
            'id_dm': id_dm,
            'created_at': status.created_at,
            'text': status.text,
            'entities': status.entities,
            'in_reply_to_status_id': status.in_reply_to_status_id
        }

    def save_user(self, id):
        user = self.api.get_user(id)
        useravailable = self.user_model.find_one({'id': user.id})
        if useravailable is None:
            self.user_model.insert_one(user._json)
