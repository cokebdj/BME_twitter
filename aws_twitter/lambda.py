import boto3
import logging
import json
import os
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class StdOutListener(StreamListener):

    def on_data(self, data):
        text = json.loads(data)["text"]
        self.logger.info(text)
        sentiment = self.comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
        tag = sentiment['Sentiment'].capitalize()
        self.logger.info(tag)
        
        if tag in ('Positive', 'Negative'):
            score = sentiment['SentimentScore'][tag]
            payload = {'score':self.dict_tags_score[tag]*score}
            put_response = self.kinesis_client.put_record(
                           StreamName=self.twitter_stream,
                           Data=json.dumps(payload),
                           PartitionKey='score')
        return True

    def on_error(self, status):
        self.logger.info(status)

def lambda_handler(event, context):
    

    kinesis_client = boto3.client('kinesis', region_name='us-east-2')
    comprehend_client = boto3.client(service_name='comprehend', region_name='us-east-2')

    api_key = os.environ['API_KEY']
    api_secret_key = os.environ['API_SECRET_KEY']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    
    l = StdOutListener()
    l.dict_tags_score = {'Positive':1,'Negative':-1}
    l.twitter_stream = os.environ['TWITTER_STREAM']
    l.logger = logger
    l.comprehend_client = comprehend_client
    l.kinesis_client = kinesis_client
    auth = OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['#bitcoin','#Bitcoin'], languages=['en'])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Finished')
    }
