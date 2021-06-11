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

# timeline = api.home_timeline()
# for tweet in timeline:
#     print(f"{tweet.user.name} said {tweet.text}")

# tweets = api.home_timeline(count=30)
# for tweet in tweets:
#     if tweet.favorite
#     print(f"Liking tweet {tweet.id} of {tweet.author.name}")
#     api.create_favorite(tweet.id)


def main():
    with open('tweets.txt', encoding='utf-8') as f:
        for line in f:
            try:
                api.update_status(status=line)
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

if __name__ == "__main__":
    main()
