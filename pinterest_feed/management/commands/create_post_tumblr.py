# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from pinterest_feed.models import Pin, PinPublishThumblr
from django.contrib.auth.models import User
import re
import pytumblr

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('pin_id', nargs='+', type=int)

    def handle(self, *args, **options):
        c = 0
        b = 0
        for item in options['pin_id']:
            pin = Pin.objects.get(id=int(item))
            check_publish = self.create_post_tumblr(pin.text.encode('utf-8'), pin.img_url, c, b)
            if (check_publish):              
                user = User.objects.get(id=1)
                publish = PinPublishThumblr(user = user, pin_item = pin)
                publish.save() 
                c +=1
                b +=1

    def create_post_tumblr(self, title, img_url, c, b):
        client = pytumblr.TumblrRestClient(
            'cSXsJ8y4YkGsJkhwGQPnY1RIgkXUFvTRtS7MKC7QWBoKbCpwWF',
            'b8yO1HSR0eMgfjwpDjXrGnZsWqYkt0SiZl0Gq4ZhH9F0BVb1KA',
            'oKm2HhFJZN5iApkTwpbOdNMhMxW8Ds5sAScP0rfO2acGP8kfC0',
            'ipu2LoD1fGxv9shFxrMeg9RW716Y65xbJ0npuVPtslKpGppp9m'
         )


        title = re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', ' ',  title)             
        if (title == ''):
            title = ''
            

        if b % 2 == 0:
            post = client.create_photo('animegirlpin', state="queue", tags=['anime girl',], caption=title, source=str(img_url))
        else:
            post = client.create_photo('anime2018', state="queue", tags=['anime girl',], caption=title, source=str(img_url))

        result = 'id' in post
        return result

        
    