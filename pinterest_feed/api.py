from rest_framework import viewsets, generics

from .models import PinPublishThumblr, PinPublishFacebook
from serializers import ThumblrSerializer, FacebookSerializer

class PinTumblrViewGet(viewsets.ModelViewSet):
    serializer_class = ThumblrSerializer
    exclude_facebook = PinPublishFacebook.objects.all().values('pin_item')
    queryset = PinPublishThumblr.objects.exclude(id__in=exclude_facebook)

class PinFacebookViewSet(viewsets.ModelViewSet):
    serializer_class = FacebookSerializer
    queryset = PinPublishFacebook.objects.all()