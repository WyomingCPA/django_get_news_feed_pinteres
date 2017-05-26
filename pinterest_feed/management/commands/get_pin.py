# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from pinterest_feed.models import Pin
import requests
import json
import re
import os


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        module_dir = os.path.dirname(__file__)  # get current directory
        data_file = os.path.join(module_dir, 'list_board.txt')  
        f = open(data_file)
        for line in f.readlines():
            line = line[:-2]
            self.get_pins(line, 'AfJlhomOfEZJKBvo75KvQ9IeBdlgFMBq-Di3MBJDs1e0t6A9-gAAAAA')

    def get_pins(self, board, token): 
        session = requests.Session()
    
        resp = session.get('https://api.pinterest.com/v1/boards/' + board + '/pins/?access_token=' + token + '&fields=id%2Clink%2Cnote%2Curl%2Cimage%2Cmetadata')
        parsed_json = json.loads(resp.content)

        try:
            for item in parsed_json['data']:
                pin_url = item['url']
                img_url = item['image']['original']['url']
                text = item['note']
                try:
                    Pin.objects.get(link=pin_url)
                except Pin.MultipleObjectsReturned:
                    pass
                except Pin.DoesNotExist:                  
                   itemPin = Pin(text = text.encode('utf-8'), img_url = img_url, link = pin_url)
                   itemPin.save()

        except:
            print 'error ' + board


