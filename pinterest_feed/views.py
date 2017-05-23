 # -- coding: utf-8 --

from django.shortcuts import render, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .models import Pin, PinHide, PinPublish, PinPublishThumblr
from django.db.models import Q

import re

import pytumblr


def test():
    pass

@login_required()
def index():
    pass

@login_required()
def read_all_pin(request):
    hide_pin = PinHide.objects.filter(user=request.user).values('pin_item')
    publish_pin = PinPublish.objects.filter(user=request.user).values('pin_item')

    list_pin = Pin.objects.exclude(Q(id__in=hide_pin) | Q(id__in=publish_pin))
    
    paginator = Paginator(list_pin, 50)
    page = request.GET.get('page')
    try:
        list_pin = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_pin = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_pin = paginator.page(paginator.num_pages)


    return render(request, 'pinterest_feed/pin_table.html', {'list_pin': list_pin })

@login_required()
def queue_all_pin(request):
    hide_pin = PinHide.objects.filter(user=request.user).values('pin_item')

    list_pin = Pin.objects.exclude(Q(id__in=hide_pin))

    paginator = Paginator(list_pin, 50)
    page = request.GET.get('page')
    try:
        list_pin = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_pin = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_pin = paginator.page(paginator.num_pages)


    return render(request, 'pinterest_feed/pin_queue.html', {'list_pin': list_pin })

@login_required()
def read_all_tumblr(request):
    hide_pin = PinHide.objects.filter(user=request.user).values('pin_item')
    tumblr_publish_pin = PinPublishThumblr.objects.filter(user=request.user).values('pin_item')

    list_pin = Pin.objects.exclude(Q(id__in=hide_pin) | Q(id__in=tumblr_publish_pin))

    paginator = Paginator(list_pin, 50)
    page = request.GET.get('page')
    try:
        list_pin = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list_pin = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list_pin = paginator.page(paginator.num_pages)


    return render(request, 'pinterest_feed/pin_tumblr.html', {'list_pin': list_pin })


@login_required()
def action_pin(request):
    if request.method == 'POST':
        pointer_user = request.POST.getlist('pointer_user[]')
        pointer_action = request.POST.getlist('pointer_action')
        
        if (pointer_action[0] == 'delete'):
            for item in pointer_user:
                pin = Pin.objects.get(id=int(item)) 
                hide = PinHide(user = request.user, pin_item = pin, )
                hide.save()

        if (pointer_action[0] == 'add_to_queue'):
            for item in pointer_user:
                pin = Pin.objects.get(id=int(item))
                queue = PinPublish(user = request.user, pin_item = pin, )
                queue.save()

        if (pointer_action[0] == 'tumblr_publish_pin'):
            for item in pointer_user:
                pin = Pin.objects.get(id=int(item))
                create_post_tumblr(pin.text, pin.img_url)
                publish = PinPublishThumblr(user = request.user, pin_item = pin)
                publish.save() 
                 
    return redirect('/pin/')

@login_required()
def SetFilter(request):
     recent_times = request.POST.get('recent_times', '')

     request.session['recent_times'] = recent_times

     return redirect('/pin/')





 #Publish tumblr animegirlpin
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
