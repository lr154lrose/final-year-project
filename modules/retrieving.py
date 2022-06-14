import tweepy
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

consumer_key = config['CONFIG']['consumer_key']
consumer_secret = config['CONFIG']['consumer_secret']

access_token = config['CONFIG']['access_token']
access_token_secret = config['CONFIG']['access_token_secret']
user_id = config['CONFIG']['user_id']
bearer_token = config['CONFIG']['bearer_token']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


client = tweepy.Client(bearer_token)


def get_client():
    client = tweepy.Client(bearer_token)
    return client


def search_tweets(query, number_results):
    client = get_client()
    result = client.search_recent_tweets(query, tweet_fields=['geo', 'created_at'], max_results = number_results)
    return result.data