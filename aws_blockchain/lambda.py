import boto3
import logging
import json
import requests
import os
from scipy.stats import linregress
import time

    

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    kinesis_client = boto3.client('kinesis', region_name='us-east-2')
    bitcoin_url = os.environ['BITCOIN_URL']
    bitcoin_stream = os.environ['BITCOIN_STREAM']
    minutes = int(os.environ['MINS'])
    times = []
    prices = []
    
    for elem in range(minutes):
        times.append(elem)
        r = requests.get('https://blockchain.info/ticker')
        price = r.json()['EUR']['last']
        logger.info(elem)
        logger.info(price)
        prices.append(price)
        time.sleep(60)
        
    slope, intercept, r_value, p_value, std_err = linregress(times, prices)
    logger.info(slope)
    
    payload = {'slope':slope}
    put_response = kinesis_client.put_record(
                   StreamName=bitcoin_stream,
                   Data=json.dumps(payload),
                   PartitionKey='slope')
    
    return {
        'statusCode': 200
    }
