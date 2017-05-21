"""
Definition of urls for django_get_news_feed_pinteres.
"""

from datetime import datetime
from django.conf.urls import url, include
from django.contrib import admin

import pinterest_feed.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pin/', pinterest_feed.views.read_all_pin, name='read_all_pin'),
    url(r'^queue/', pinterest_feed.views.queue_all_pin, name='read_all_queue'),
    url(r'^action_pin/$', pinterest_feed.views.action_pin, name='action_pin'),
    url(r'^SetFilter/$', pinterest_feed.views.SetFilter, name='SetFilter'),
]
