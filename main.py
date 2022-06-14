from tabnanny import check
import tweepy
from modules.retrieving import search_tweets
from modules.filtering import filter_tweet
import csv
import requests
import configparser


config = configparser.ConfigParser()
config.read('example_config.ini')

url = 'https://api.twitter.com/1.1/geo/id/'

consumer_key = config['CONFIG']['consumer_key']
consumer_secret = config['CONFIG']['consumer_secret']

access_token = config['CONFIG']['access_token']
access_token_secret = config['CONFIG']['access_token_secret']
user_id = config['CONFIG']['user_id']
bearer_token = config['CONFIG']['bearer_token']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
search_headers = {
    'Authorization': 'Bearer {}'.format(bearer_token)    
}


def check_english(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def write_csv(path, data, search_term):

    with open(path, 'a', encoding='utf-8', newline='') as f:
        for row in data:
            
            if(check_english(row.text)):
                if row.geo:
                    location_url = url + str(row.geo['place_id']) + ".json"
                    print(location_url)
                    resp = requests.get(url=location_url, headers=search_headers)
                    location_data = resp.json()
                    if('coordinates' in location_data): location_coordinates = location_data['coordinates']['coordinates']
                    else: location_coordinates = location_data['centroid']
                    f.write(filter_tweet(str(row.text))+','+search_term+','+location_data['country']+','+str(row.created_at).split(' ')[0]+','+str(location_coordinates)+'\n')

                else: f.write(filter_tweet(str(row.text))+','+search_term+','+'None'+','+str(row.created_at).split(' ')[0]+','+'None'+'\n')


def construct_result(data):
    result = []
    if data:
        for tweet in data:
            result.append(tweet)

    else:
        result = None

    return result


if __name__ == "__main__":
    search_terms = ['lake blue green algae cyanotoxin', 'cyanotoxin', 'water quality', 'algae cyanotoxin', 'bacteria cyanotoxin', 'bloom cyanotoxin', 'toxic', 'poisonous water cyanotoxin', 'wildlife cyanotoxin', 'livestock death', 'mass mortality', 'mortality animals', 'fish kills', 'pond water quality cyanotoxin', 'lake water quality', 'sea bacteria', 'beach water quality', 'sick animals bacteria', 'sick fish bacteria', 'elephant death', 'cattle sick bacteria', 'livestock kills cyanobacteria', 'livestock sick cyanobacteria', 'livestock death', 'phytoplankton', 'blue green algae', 'shore animal death', 'hippo death', 'flamingo sick', 'pond cyanobacteria', 'wildlife rash', 'wildlife crooked neck', 'wildlife seizure', 'elephant sick', 'cattle deaths cyanobacteria', 'fish deaths cyanobacteria', 'cyanotoxin deaths', 'cyanotoxin kill', 'cyanobacteria kills', 'cyanobacteria deaths', 'cyanobacteria pond', 'cyanobacteria water', 'cyanotoxin water', 'bird sick cyanobacteria', 'bird deaths cyanobacteria', 'pets cyanobacteria', 'animals cyanotoxins', 'blue green algae animals', 'blue green algae water', 'blue green algae water quality', 'toxic bloom']
    search_results = 100
    path_csv = './datasets/tweets.csv'

    for search_term in search_terms:
    
        tweets = search_tweets(search_term, search_results)

        data = construct_result(tweets)
        if data:
            write_csv(path_csv, data, search_term)