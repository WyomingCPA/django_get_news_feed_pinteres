# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from pinterest_feed.models import Pin, PinPublishThumblr, SettingsModel

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('pin_id', nargs='+', type=int)

    def handle(self, *args, **options):

        s1 = SettingsModel(False)
        s1.save()

        for item in options['pin_id']:
            pin = Pin.objects.get(id=int(item))
            create_post_tumblr(pin.text.encode('utf-8'), pin.img_url)
            publish = PinPublishThumblr(user = request.user, pin_item = pin)
            publish.save() 

        s2 = SettingsModel(True)
        s2.save()

    def create_post_tumblr(title, img_url):
        client = pytumblr.TumblrRestClient(
            'cSXsJ8y4YkGsJkhwGQPnY1RIgkXUFvTRtS7MKC7QWBoKbCpwWF',
            'b8yO1HSR0eMgfjwpDjXrGnZsWqYkt0SiZl0Gq4ZhH9F0BVb1KA',
            'oKm2HhFJZN5iApkTwpbOdNMhMxW8Ds5sAScP0rfO2acGP8kfC0',
            'ipu2LoD1fGxv9shFxrMeg9RW716Y65xbJ0npuVPtslKpGppp9m'
         )


        title = re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', ' ',  title)             
        if (title == ''):
            title = ''
            
        Tagss = title.split()
        listTag = []
        for tag in Tagss:
            if "." in tag:
                tag = tag.replace('.', '')
                listTag.append(tag)
                continue

            elif "," in tag:
                tag = tag.replace(',', '')
                listTag.append(tag)
                continue

            listTag.append(tag)

        client.create_photo('animegirlpin', state="queue", link='animegirlpin.tumblr.com', tags=listTag[:4], caption=title, source=str(img_url))


    