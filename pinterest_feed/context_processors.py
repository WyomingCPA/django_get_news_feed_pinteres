from .models import Pin, PinHide, PinPublish, PinPublishThumblr
from django.db.models import Q

from django.contrib.auth.models import User

def count_category(request):
    try:
        hide_pin = PinHide.objects.filter(user=request.user).values('pin_item')
        publish_pin = PinPublish.objects.filter(user=request.user).values('pin_item')
        all_pin = Pin.objects.exclude(Q(id__in=hide_pin) | Q(id__in=publish_pin)).count()

    except:
        all_pin = 0

    try:
         hide_pin = PinHide.objects.filter(user=request.user).values('pin_item')
         queue_pin = Pin.objects.exclude(Q(id__in=hide_pin)).count()

    except:
        queue_pin = 0

    try:
        hide_pin = PinHide.objects.filter(user=request.user).values('pin_item')
        tumblr_publish_pin = PinPublishThumblr.objects.filter(user=request.user).values('pin_item')
        tumblr_pin = Pin.objects.exclude(Q(id__in=hide_pin) | Q(id__in=tumblr_publish_pin)).count()

    except:
        tumblr_pin = 0



    return { 'all_pin': all_pin, 'queue_pin': queue_pin, 'tumblr_pin' : tumblr_pin, }
