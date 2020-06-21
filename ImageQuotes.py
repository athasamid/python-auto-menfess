from PIL import Image, ImageFont, ImageDraw
from io import StringIO
import requests
import textwrap
from random import randint
import glob


class ImageQuotes(object):
    def __init__(self, tweet, username):
        self.tweet = tweet
        self.username = username

    def makeImage(self):
        imagelist = glob.glob('images/img*.jpg')

        image = Image.open(imagelist[randint(0, len(imagelist) - 1)])
        draw = ImageDraw.Draw(image)
        width, height = image.size

        bg = Image.new("RGBA", (int(width), int(height)), (0, 0, 0, 127))
        image.paste(bg, (0, 0), bg)

        header = self.draw_header(width, height)
        w_header, h_header = header.size

        tot_height = 0
        color = 'rgb(255, 255, 255)'

        tot_height += h_header

        message = self.tweet.text
        lines = textwrap.wrap(message, width=50)

        image_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=20)

        wtext = 0
        for line in lines:
            w, h = image_font.getsize(line)
            tot_height += h
            if wtext < w:
                wtext = w

        x_text = (width - wtext) / 2
        y_text = (height - tot_height) / 2

        image.paste(header, (int(x_text), int(y_text)), header)
        y_text += h_header + 10

        for line in lines:
            w, h = image_font.getsize(line)
            draw.text((x_text, y_text), line, fill=color, font=image_font)
            y_text += h

        footer = self.draw_footer()
        wfooter, hfooter = footer.size
        image.paste(footer, (width - wfooter - 10, 10), footer)

        image.save('quotes/' + self.tweet.id_str + '.jpg')

        return {'path': 'quotes/' + self.tweet.id_str + '.jpg', 'name': self.tweet.id_str + '.jpg'}

    def draw_footer(self):
        logo = Image.open("images/twitter.png")
        font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=20)
        name = self.username

        logo = logo.resize((20, 20), Image.ANTIALIAS)

        wf, hf = font.getsize(name)
        wl, hl = logo.size

        width = wf + wl + 50
        height = hl

        frame = Image.new("RGBA", (int(width), int(height)))
        draw = ImageDraw.Draw(frame)
        frame.paste(logo, (0, 0))
        draw.text((int(wl + 25), int((hf - hl) / 2)), name, font=font, fill="RGB(255, 255, 255)")

        return frame

    def draw_header(self, width, height):
        name = self.tweet.user.name
        screenname = '@' + self.tweet.user.screen_name

        profile = self.draw_profile_image(img_url=self.tweet.user.profile_image_url.replace('_normal', ''), width=width, height=height)
        user_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=20)

        print(profile.size)

        wscreenname, hscreenname = user_font.getsize(screenname)
        wname, hname = user_font.getsize(name)
        wprofile, hprofile = profile.size

        wtext = wscreenname
        if wscreenname < wname:
            wtext = wname

        frame = Image.new("RGBA", (int(wtext + wprofile + 50), int(hprofile)))
        draw = ImageDraw.Draw(frame)

        ytext = (hprofile - (hscreenname + hname)) / 2
        xtext = wprofile + 25

        draw.text(text=name, xy=(int(xtext), int(ytext)), fill='rgb(255, 255, 255)', font=user_font)
        ytext += hname
        draw.text(text=screenname, xy=(int(xtext), int(ytext)), fill='rgb(255, 255, 255)', font=user_font)
        frame.paste(profile, (0, 0))

        # frame.save("quotes/frame.png")

        return frame

    def draw_profile_image(self, img_url, width, height):
        profile = Image.open(requests.get(img_url, stream=True).raw)
        w_profile, h_profile = profile.size
        print(profile.size)
        bigsize = (int(w_profile/4) * 3, int(h_profile/4) * 3)
        mask = Image.new('L', bigsize, 0)
        maskdraw = ImageDraw.Draw(mask)
        maskdraw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(profile.size, Image.ANTIALIAS)
        profile.putalpha(mask)
        profile = profile.resize((int(w_profile/4), int(h_profile/4)), Image.ANTIALIAS)
        return profile

# if __name__ == "__main__":
#     tweet = {'contributors': None, 'coordinates': None, 'created_at': 'Fri Jan 10 21:28:07 +0000 2020',
#              'display_text_range': [22, 44],
#              'entities': {'hashtags': [{'indices': [34, 44], 'text': 'bjnfessrt'}], 'symbols': [], 'urls': [],
#                           'user_mentions': [{'id': 276336536, 'id_str': '276336536', 'indices': [0, 10],
#                                              'name': 'Dhimas Atha Abdillah', 'screen_name': 'athasamid'},
#                                             {'id': 513407996, 'id_str': '513407996', 'indices': [11, 21],
#                                              'name': 'babang grab +62 341', 'screen_name': 'IskhakM88'},
#                                             {'id': 483456845, 'id_str': '483456845', 'indices': [22, 33],
#                                              'name': 'Auto Bojonegoro Menfess', 'screen_name': 'botbjnfess'}]},
#              'favorite_count': 0, 'favorited': False, 'filter_level': 'low', 'geo': None, 'id': 1215747170046840832,
#              'id_str': '1215747170046840832', 'in_reply_to_screen_name': 'athasamid',
#              'in_reply_to_status_id': 1214987730926522368, 'in_reply_to_status_id_str': '1214987730926522368',
#              'in_reply_to_user_id': 276336536, 'in_reply_to_user_id_str': '276336536', 'is_quote_status': False,
#              'lang': 'und', 'place': None, 'quote_count': 0, 'reply_count': 0, 'retweet_count': 0, 'retweeted': False,
#              'source': '<a href="https://mobile.twitter.com" rel="nofollow">Twitter Web App</a>',
#              'text': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
#              'timestamp_ms': '1578691687486', 'truncated': False,
#              'user': {'contributors_enabled': False, 'created_at': 'Thu Jun 16 21:59:43 +0000 2016',
#                       'default_profile': True, 'default_profile_image': False,
#                       'description': 'B-kul Baku Kuliner  aplikasi marketplace kuliner berbasis web dan mobile android yang berguna untuk mencari informasi mengenai kuliner yg berada diwilayah Jatim',
#                       'favourites_count': 0, 'follow_request_sent': None, 'followers_count': 4, 'following': None,
#                       'friends_count': 0, 'geo_enabled': False, 'id': 743563732375113732,
#                       'id_str': '743563732375113732', 'is_translator': False, 'lang': None, 'listed_count': 0,
#                       'location': 'Malang, Jawa Timur', 'name': 'b-kul kuliner', 'notifications': None,
#                       'profile_background_color': 'F5F8FA', 'profile_background_image_url': '',
#                       'profile_background_image_url_https': '', 'profile_background_tile': False,
#                       'profile_image_url': 'http://pbs.twimg.com/profile_images/743564209112252416/kCmnqIFJ_normal.jpg',
#                       'profile_image_url_https': 'https://pbs.twimg.com/profile_images/743564209112252416/kCmnqIFJ_normal.jpg',
#                       'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED',
#                       'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333',
#                       'profile_use_background_image': True, 'protected': False, 'screen_name': 'bkul_kuliner',
#                       'statuses_count': 10, 'time_zone': None, 'translator_type': 'none', 'url': None,
#                       'utc_offset': None, 'verified': False}}
#     imagesquotes = ImageQuotes(tweet, "@bjnfess")
#     imagesquotes.makeImage()
