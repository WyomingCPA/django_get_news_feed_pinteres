from rest_framework import viewsets, generics

from django.db.models import Q

from .models import PinPublishThumblr, PinPublishFacebook, Pin, PinHide
from serializers import ThumblrSerializer, FacebookSerializer



class PinTumblrViewGet(viewsets.ModelViewSet):
    serializer_class = ThumblrSerializer

    exclude_facebook = PinPublishFacebook.objects.all().values('pin_item')
    exclude_hidden = PinHide.objects.all().values('pin_item')
    tumblr_publish_pin = PinPublishThumblr.objects.all().values('pin_item')

    queryset = Pin.objects.exclude(Q(id__in=exclude_facebook) | Q(id__in=exclude_hidden)).filter(id__in=tumblr_publish_pin)[:50]

class PinFacebookViewSet(viewsets.ModelViewSet):
    serializer_class = FacebookSerializer
    queryset = PinPublishFacebook.objects.all()