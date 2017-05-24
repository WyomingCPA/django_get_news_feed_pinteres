 # -- coding: utf-8 --

from django.shortcuts import render, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .models import Pin, PinHide, PinPublish, PinPublishThumblr
from django.db.models import Q

from django.core.management import call_command





def test():
    pass

@login_required()
def index():
    pass

@login_required()
def read_all_pin(request):
    hide_pin = PinHide.objects.filter(user=request.user).values('pin_item')
    publish_pin = PinPublish.objects.filter(user=request.user).values('pin_item')
    tumblr_publish_pin = PinPublishThumblr.objects.filter(user=request.user).values('pin_item')

    list_pin = Pin.objects.exclude(Q(id__in=hide_pin) | Q(id__in=publish_pin) | Q(id__in=tumblr_publish_pin))
    
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
    publish_pin = PinPublish.objects.filter(user=request.user).values('pin_item')
    tumblr_publish_pin = PinPublishThumblr.objects.filter(user=request.user).values('pin_item')

    list_pin = Pin.objects.exclude(Q(id__in=hide_pin) | Q(id__in=tumblr_publish_pin)).filter(id__in=publish_pin)

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
    publish_pin = PinPublish.objects.filter(user=request.user).values('pin_item')

    list_pin = Pin.objects.exclude(Q(id__in=hide_pin) | Q(id__in=tumblr_publish_pin)).filter(id__in=publish_pin)

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
            call_command('create_post_tumblr' ,*pointer_user)

                 
    return redirect('/pin/')

@login_required()
def SetFilter(request):
     recent_times = request.POST.get('recent_times', '')

     request.session['recent_times'] = recent_times

     return redirect('/pin/')



