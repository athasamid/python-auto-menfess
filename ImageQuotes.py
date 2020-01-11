from PIL import Image, ImageFont, ImageDraw


class ImageQuotes(object):
    def __init__(self, tweet):
        self.tweet = tweet

    def makeImage(self):
        image = Image.open('images/img1.jpg')
        draw = ImageDraw.Draw(image)

        width, height = image.size()

        image_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", size=42)
        (x, y) = (50, 50)
        message = "Test gambar"
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), message, fill=color, font=image_font)

        (x, y) = (150, 150)
        name = 'Vinay'
        color = 'rgb(255, 255, 255)'
        draw.text((x, y), name, fill=color, font=image_font)


