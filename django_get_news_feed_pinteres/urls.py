"""
Definition of urls for django_get_news_feed_pinteres.
"""

from datetime import datetime
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

import pinterest_feed.views

from pinterest_feed.api import PinTumblrViewGet, PinFacebookViewSet

router = routers.DefaultRouter()
router.register(r'tumblr', PinTumblrViewGet)
router.register(r'facebook', PinFacebookViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^pin/', pinterest_feed.views.read_all_pin, name='read_all_pin'),
    url(r'^queue/', pinterest_feed.views.queue_all_pin, name='read_all_queue'),
    url(r'^tumblr/', pinterest_feed.views.read_all_tumblr, name='read_all_tumblr'),
    url(r'^action_pin/$', pinterest_feed.views.action_pin, name='action_pin'),
    url(r'^SetFilter/$', pinterest_feed.views.SetFilter, name='SetFilter'),
]
