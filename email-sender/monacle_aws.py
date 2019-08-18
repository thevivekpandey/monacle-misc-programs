import gzip
import sys, os
import shutil
import json
import boto3
import logging

def get_sqs_boto_conn(credentials, resource):
    access_key = credentials['key']
    access_secret = credentials['secret']
    region_name = credentials['region_name']
    boto3.setup_default_session(aws_access_key_id=access_key,
                                aws_secret_access_key=access_secret,
                                region_name=region_name)
    return boto3.resource(resource)

def send_sqs_message(message):
    sqs_credentials = {
        'key': os.getenv('EMAIL_SQS_KEY'),
        'secret': os.getenv('EMAIL_SQS_SECRET'),
        'region_name': os.getenv('EMAIL_SQS_REGION_NAME')
    }
    try:
        sqs = get_sqs_boto_conn(sqs_credentials, 'sqs')
        queue = sqs.get_queue_by_name(QueueName='email')
        queue.send_message(MessageBody=json.dumps(message))
    except Exception as e:
        print(e)

def receive_sqs_message():
    sqs_credentials = {
        'key': os.getenv('EMAIL_SQS_KEY'),
        'secret': os.getenv('EMAIL_SQS_SECRET'),
        'region_name': os.getenv('EMAIL_SQS_REGION_NAME')
    }
    try:
        sqs = get_sqs_boto_conn(sqs_credentials, 'sqs')
        queue = sqs.get_queue_by_name(QueueName='email')
        return queue
    except Exception as e:
        print(e)
        return None
