from rest_framework import viewsets, generics

from .models import PinPublishThumblr, PinPublishFacebook, Pin
from serializers import ThumblrSerializer, FacebookSerializer

class PinTumblrViewGet(viewsets.ModelViewSet):
    serializer_class = ThumblrSerializer
    exclude_facebook = PinPublishFacebook.objects.all().values('pin_item')
    queryset = Pin.objects.exclude(id__in=exclude_facebook)[:50]

class PinFacebookViewSet(viewsets.ModelViewSet):
    serializer_class = FacebookSerializer
    queryset = PinPublishFacebook.objects.all()