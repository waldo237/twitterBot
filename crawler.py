import tweepy
from decouple import config
import json
import datetime
CONSUMER_KEY = config('KEY')
CONSUMER_SECRET = config('SECRET')
ACCESS_TOKEN = config('ACCESS')
ACCESS_SECRET = config('ACCESS_SECRET')

 
class TweetCrawler(object):

    result_limit = 20
    data = []
    api = False

    twitter_keys = {
        'consumer_key':        CONSUMER_KEY,
        'consumer_secret':     CONSUMER_SECRET,
        'access_token_key':    ACCESS_TOKEN,
        'access_token_secret': ACCESS_SECRET
    }

    def __init__(self, keys_dict=twitter_keys, api=api, result_limit=5):

        self.twitter_keys = keys_dict
        auth = tweepy.OAuthHandler(
            keys_dict['consumer_key'], keys_dict['consumer_secret'])
        auth.set_access_token(
            keys_dict['access_token_key'], keys_dict['access_token_secret'])

        self.api = tweepy.API(auth)

        self.result_limit = result_limit

    def mine_user_tweets(self, user='waldoMilanes', 
                         mine_rewteets=False,
                         max_pages=1):
        user = self.api.me()
        data = []
        last_tweet_id = False
        page = 1

        while page <= max_pages:
            if last_tweet_id:
                statuses = self.api.user_timeline(screen_name=user,
                                                  count=self.result_limit,
                                                  max_id=last_tweet_id - 1,
                                                  tweet_mode='extended',
                                                  include_retweets=False
                                                  )
            else:
                statuses = self.api.user_timeline(screen_name=user,
                                                  count=self.result_limit,
                                                  tweet_mode='extended',
                                                  include_retweets=False)

            for item in statuses:

                mined = {
                    'tweet_id':        item.id,
                    'name':            item.user.name,
                    'screen_name':     item.user.screen_name,
                    'retweet_count':   item.retweet_count,
                    'text':            item.full_text,
                    'mined_at':        datetime.datetime.now(),
                    'created_at':      item.created_at,
                    'favourite_count': item.favorite_count,
                    'hashtags':        item.entities['hashtags'],
                    'status_count':    item.user.statuses_count,
                    'location':        item.place,
                    'source_device':   item.source
                }

                try:
                    mined['retweet_text'] = item.retweeted_status.full_text
                except:
                    mined['retweet_text'] = None
                try:
                    mined['quote_text'] = item.quoted_status.full_text
                    mined['quote_screen_name'] = statuses.quoted_status.user.screen_name
                except:
                    mined['quote_text'] = None
                    mined['quote_screen_name'] = None

                last_tweet_id = item.id
                data.append(mined)

            page += 1
            print(data)
        with open('collected_tweets.json', 'w+') as f:
            f.write(json.dumps(data,indent=4, sort_keys=True, default=str))
        return data

if __name__ == "__main__":
    tc = TweetCrawler()
    tc.mine_user_tweets()