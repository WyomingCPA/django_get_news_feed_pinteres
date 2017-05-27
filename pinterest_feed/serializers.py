from .models import PinPublishThumblr, PinPublishFacebook, Pin

from django.contrib.auth.models import User

from rest_framework import serializers

class ThumblrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'


class FacebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinPublishFacebook
        fields = '__all__'