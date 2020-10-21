import json
import logging
import os
from datetime import datetime, timedelta
from numpy import mean
from scipy.stats import linregress
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_records(STREAM_NAME, MINUTES_BACK):
    kinesis = boto3.client('kinesis', region_name='us-east-2')
    kinesis_stream = kinesis.describe_stream(StreamName=STREAM_NAME)
    shards = kinesis_stream['StreamDescription']['Shards']
    shard_ids = [shard['ShardId'] for shard in shards]
    now = datetime.now()
    pre = now - timedelta(minutes=MINUTES_BACK)
    iter_response = kinesis.get_shard_iterator(StreamName=STREAM_NAME, ShardId=shard_ids[0], ShardIteratorType="AT_TIMESTAMP", Timestamp=pre.microsecond)
    shard_iterator = iter_response['ShardIterator']
    record_response = kinesis.get_records(ShardIterator=shard_iterator)
    data = [json.loads(record['Data']) for record in record_response['Records']]
    return data


def lambda_handler(event, context):
    
    bitcoin_stream = os.environ['BITCOIN_STREAM']
    twitter_stream = os.environ['TWITTER_STREAM']
    minutes_pre = int(os.environ['MINUTES_PRE'])
    topic_arn_msg = os.environ["TOPIC_ARN"]
    
    threshold_sent_count = float(os.environ['THRESHOLD_SENT_COUNT'])
    threshold_sent_value = float(os.environ['THRESHOLD_SENT_VALUE'])
    threshold_bitcoin_r = float(os.environ['THRESHOLD_BITCOIN_R'])
    threshold_bitcoin_slope = float(os.environ['THRESHOLD_BITCOIN_SLOPE'])
    
    logger.info(f"Sentiment: count limit {threshold_sent_count}, value limit {threshold_sent_value}")
    logger.info(f"Bitcoin: r limit {threshold_bitcoin_r}, slope limit {threshold_bitcoin_slope}")
    
    data_sentiment = get_records(twitter_stream, minutes_pre)
    scores = [elem['score'] for elem in data_sentiment]
    sent_value = mean(scores)
    sent_count = len(scores)
    
    logger.info(f"Obtained sentiment: count {sent_count}, value {sent_value}")
    
    data_bitcoin = get_records(bitcoin_stream, minutes_pre)
    times = [time for time, price in enumerate(data_bitcoin)]
    prices = [price['price'] for price in data_bitcoin]
    slope, intercept, r_value, p_value, std_err = linregress(times, prices)
    
    logger.info(f"Bitcoin: r {r_value}, slope {slope}")
    
    bool_slope = slope > threshold_bitcoin_slope
    bool_r = r_value > threshold_bitcoin_r
    bool_count = sent_count > threshold_sent_count
    bool_score = sent_value > threshold_sent_value
    
    if bool_slope and bool_r and bool_count and bool_score:
    
        sns = boto3.client('sns')
        text = f""" From the last {minutes_pre} minutes we have noticed a sentiment metric of {round(sent_value,2)} with as much as {round(sent_count,2)} mentions!!! Also slope is {round(slope,2)} with an r of {round(r_value,2)}. Good time for buying Bitcoin! """
        sns.publish(TopicArn=topic_arn_msg,
                    Subject='good time for buying bitcoin',
                    Message=text)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Analyzed!')
    }
