# -*- coding: utf-8 -*-

import boto3
import os
import urllib
import urllib2

def handler(event, context):
    task_name = event['resources'][0].split('/')[1]
    aws_api_endpoint = os.environ['AWS_API_ENDPOINT']
    text = "<b>%s</b> 알림이 발생했습니다. [<a href=\"%s/utils/reminder/tasks/%s?isDone=true\">작업완료</a>]" % (task_name, aws_api_endpoint, task_name)

    data = {
        'chat_id': os.environ['TELEGRAM_CHAT_ID'],
        'text': text,
        'parse_mode': 'HTML'
    }

    request = urllib2.Request(os.environ['TELEGRAM_URL'], data=urllib.urlencode(data))
    urllib2.urlopen(request)
