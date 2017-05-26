# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#Модель pin'a
class Pin(models.Model):
    text = models.CharField(max_length=2000)
    link = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)
    time_parsing = models.DateTimeField(auto_now = True)

#Скрыть pin 
class PinHide(models.Model):
    user = models.ForeignKey(User)
    pin_item = models.ForeignKey(Pin)
    time_update = models.DateTimeField(auto_now = True)

#pin на публикацию
class PinPublish(models.Model):
    user = models.ForeignKey(User)
    pin_item = models.ForeignKey(Pin)
    time_update = models.DateTimeField(auto_now = True)

#Опубликованный в Thumlblr
class PinPublishThumblr(models.Model):
    user = models.ForeignKey(User)
    pin_item = models.ForeignKey(Pin)
    time_update = models.DateTimeField(auto_now = True)

#Опубликованный в Facebook
class PinPublishFacebook(models.Model):
    user = models.ForeignKey(User)
    pin_item = models.ForeignKey(Pin)
    time_update = models.DateTimeField(auto_now = True)




class SettingsModel(models.Model):
    successOperation = models.BooleanField(default=True)

    def save(self):
        self.pk = 1
        super(SettingsModel, self).save()





