# from os import sep
import tweepy
from decouple import config
import time
import pandas as pd
import asyncio
import photo_finder as pf

CONSUMER_KEY = config('KEY')
CONSUMER_SECRET = config('SECRET')
ACCESS_TOKEN = config('ACCESS')
ACCESS_SECRET = config('ACCESS_SECRET')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class TweetBot:
    def __init__(self, api):
        self.api = api

    async def like_and_follow_replies(self, count):
        timeline = api.mentions_timeline(count)
        for tweet in timeline:
            if not tweet.user.following:
                tweet.user.follow()
                print(f"just followed {tweet.user.name}", now())
            if not tweet.favorited:
                tweet.favorite()
                print(f"liked {tweet.user.name}'s reply: {tweet.text}", now())

    async def tweet_from_a_file(self, fname):
        """ tweets the lines from a file every 40 minutes."""
        csv = pd.read_csv(fname)

        for i, v in enumerate(csv.values):
            tweet = v[0]
            if not "already_tweeted" in tweet:
                self.api.update_with_media(pf.find_photo(), status=tweet)
                csv.loc[i, 'tweets'] = tweet + " already_tweeted"
                csv.to_csv(fname, index=False)
                print(f"Just tweeted {tweet}", now())
                break

    async def like_home_tweets(self, num_tweets=20):
        tweets = self.api.home_timeline(count=num_tweets)
        for tweet in tweets:
            if not tweet.favorited and tweet.author != api.me():
                print(f"Liking tweet {tweet.id} of {tweet.author.name}", now())
                tweet.favorite()


def now():
    return '-->' + time.ctime(time.time())

async def main():
    bot = TweetBot(api)
    try:
        while True:
            await asyncio.create_task(bot.tweet_from_a_file('tweets.csv'))
            await asyncio.sleep(1)
            await asyncio.create_task(bot.like_and_follow_replies(10))
            await asyncio.sleep(1)
            await asyncio.create_task(bot.like_home_tweets(5))
            print('see you in 1 hour', now())
            await asyncio.sleep(60*60)
    except tweepy.TweepError as e:
        print(e.reason)
    except tweepy.RateLimitError:
        await asyncio.sleep(15*60)
    except  Exception as e:
        print('there was an error', e)

if __name__ == "__main__":
    asyncio.run(main())
