import tweepy
from decouple import config
import time

CONSUMER_KEY = config('KEY')
CONSUMER_SECRET = config('SECRET')
ACCESS_TOKEN = config('ACCESS')
ACCESS_SECRET = config('ACCESS_SECRET')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


class TweetBot:
    def __init__(self, api):
        self.api = api

    def like_and_follow_replies(self, count):
        timeline = api.mentions_timeline(count)
        for tweet in timeline:
            try:
                print(f"{tweet.user.name} said {tweet.text}")
                if not tweet.user.following:
                    tweet.user.follow()
                if not tweet.favorited:
                    tweet.favorite()
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(3)
                continue
            except tweepy.RateLimitError:
                time.sleep(15*60)
            except StopIteration:
                break

    def tweet_from_a_file(self, file):
        """ tweets the lines from a file every 15 minutes."""
        with open(file, encoding='utf-8') as f:
            for line in f:
                try:
                    self.api.update_status(status=line)
                    print("Will Tweet in 15 minutes")
                    time.sleep(900)
                except tweepy.TweepError as e:
                    print(e.reason)
                    time.sleep(3)
                    continue
                except tweepy.RateLimitError:
                    time.sleep(15*60)
                except StopIteration:
                    break

    def like_home_tweets(self, num_tweets=20):
        tweets = self.api.home_timeline(count=num_tweets)
        for tweet in tweets:
            try:
                print(f"Liking tweet {tweet.id} of {tweet.author.name}")
                if not tweet.favorited:
                    tweet.favorite()
                
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(3)
                continue
            except tweepy.RateLimitError:
                time.sleep(15*60)
            except StopIteration:
                break


if __name__ == "__main__":
    bot = TweetBot( api)
    # bot.tweet_from_a_file('tweets.txt')
    bot.like_home_tweets(40)