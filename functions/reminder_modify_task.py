# -*- coding: utf-8 -*-

import boto3

def handler(event, context):
    name = event['name']
    is_done = event['isDone']

    client = boto3.client('dynamodb')

    response = client.get_item(
        TableName='ReminderTask',
        Key={
            'Name': {
                'S': name
            }
        }
    )
    item = response['Item']
    item['IsDone'] = {
        'BOOL': is_done
    }

    client.put_item(
        TableName='ReminderTask',
        Item=item
    )

    return "success"
