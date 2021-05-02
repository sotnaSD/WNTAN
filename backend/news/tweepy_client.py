from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy import API
import pandas as pd
import pickle
import credentials


pd.set_option('display.max_columns', None)


class TwitterClient():
    def __init__(self):
        print('Connection to Twitter API started.')
        self.builder = DataBulider()
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        print('  Auth successful.')

    def get_user_timeline_tweets(self, filename='data', twitter_users=None, n_tweets=10):
        tweets = []
        print('  Fetching tweets...')
        for twitter_user in twitter_users:
            for tweet in Cursor(self.twitter_client.user_timeline, id=twitter_user, tweet_mode='extended').items(n_tweets):
                tweets.append(self.builder.format_tweet(tweet))

        print('  Tweets retrieved.')

        self.save_tweets(filename, tweets)

    def save_tweets(self, filename, data):
        df = pd.DataFrame(data=data, columns=['text'])

        with open('../data/' + filename, 'wb') as fp:
            pickle.dump(df, fp)

        print('  File with tweets generated.')


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        return auth

class DataBulider():

    def format_tweet(self, status):
        print(status)
        return
        full_text = self.get_full_text(status)
        return full_text

    def get_full_text(self, status):
        if status._json.get('full_text'):
            full_text = status.full_text
        else:
            if status._json.get('extended_tweet'):
                full_text = status._json.get('extended_tweet').get('full_text')
            else:
                if status._json.get('retweeted_status'):
                    if status._json.get('retweeted_status').get('extended_tweet'):
                        full_text = status._json.get('retweeted_status').get('extended_tweet').get('full_text')
                    else:
                        full_text = status._json.get('retweeted_status').get('text')
                else:
                    full_text = status.text
        return full_text


screen_names_list = ['CCInoticias']
# fetched_tweets_filename = 'tweets.p'
fetched_tweets_filename = 'tweetsTesting.p'


twitter_client = TwitterClient()
twitter_client.get_user_timeline_tweets(fetched_tweets_filename, screen_names_list, 1)


