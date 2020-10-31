import boto3
import logging
import json
import requests
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    kinesis_client = boto3.client('kinesis', region_name='us-east-2')
    bitcoin_url = os.environ['BITCOIN_URL']
    bitcoin_stream = os.environ['BITCOIN_STREAM']
    r = requests.get(bitcoin_url)
    price = r.json()['EUR']['last']
    logger.info(price)

    payload = {'price': price}
    put_response = kinesis_client.put_record(
                   StreamName=bitcoin_stream,
                   Data=json.dumps(payload),
                   PartitionKey='price')
    
    return {
        'statusCode': 200
    }
