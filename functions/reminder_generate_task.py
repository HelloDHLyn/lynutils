# -*- coding: utf-8 -*-

import boto3

def generate_events_rule(name, datetime):
    """
    CloudWatch Events 규칙을 생성한다.
    """
    import uuid
    from dateutil import parser

    result = parser.parse(datetime)
    cron_expression = 'cron(%d %d %d %d ? %d)' % (result.minute, result.hour, result.day, result.month, result.year)

    events_client = boto3.client('events')
    lambda_client = boto3.client('lambda')

    # CloudWatch Events 규칙을 등록한다.
    response = events_client.put_rule(
        Name=name,
        ScheduleExpression=cron_expression,
        State='ENABLED'
    )

    # 이벤트 타깃 Lambda 함수를 불러온다.
    lambda_obj = lambda_client.get_function(
        FunctionName='reminderNotify'
    )
    lambda_arn = lambda_obj['Configuration']['FunctionArn']

    # Events 규칙에 타깃을 추가한다.
    events_client.put_targets(
        Rule=name,
        Targets=[
            {
                'Id': str(uuid.uuid4()),
                'Arn': lambda_arn
            }
        ]
    )

    return response['RuleArn']

def put_task_to_dynamodb(name, rule_arn):
    """
    DynamoDB에 Task를 삽입한다.
    """
    client = boto3.client('dynamodb')
    response = client.put_item(
        TableName='ReminderTask',
        Item={
            'Name': {
                'S': name
            },
            'RuleArn': {
                'S': rule_arn
            },
            'IsDone': {
                'BOOL': False
            }
        }
    )

def handler(event, context):
    name = event['name']
    datetime = event['datetime']

    rule_arn = generate_events_rule(name, datetime)
    put_task_to_dynamodb(name, rule_arn)

    return "complete"
