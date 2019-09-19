import tweepy
import time
import random
import reddit
import config

# twitter auth
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret
# twitter object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def follow_back():
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        print("followed " + follower.name)


def retweet():
    search = "amazing facts"
    num_of_tweets = 10
    for tweet in tweepy.Cursor(api.search, search).items(num_of_tweets):
        try:
            tweet.retweet()
        except tweepy.TweepError as e:
            print(e)


def reply(since_id):
    print("retrieving mentions...")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        # Jokes
        if any(keyword in tweet.text.lower() for keyword in ['joke', 'jokes']):
            f = open('joke.txt', mode='r')
            jokes = [joke.rstrip() for joke in f.readlines()]
            j = random.choice(jokes)
            f.close()
            print("answering to " + tweet.user.screen_name)
            try:
                status = "@{} ".format(tweet.user.screen_name)
                api.update_status(status=status + j, in_reply_to_status_id=tweet.id)
            except tweepy.TweepError:
                pass
        elif any(keyword in tweet.text.lower() for keyword in ["interesting"]):
            print("answering to " + tweet.user.screen_name)
            try:
                post = reddit.interesting()
                rep = "@{} ".format(tweet.user.screen_name)
                status = "Here's something interesting from reddit-\n" + post['title'] + '\n' + post['url']
                api.update_status(status=rep + status, in_reply_to_status_id=tweet.id)
            except tweepy.TweepError as e:
                print(e.reason)
        # Reply Hello
        elif any(keyword in tweet.text.lower() for keyword in ["hello", "hey", "hi"]):
            print("answering to " + tweet.user.screen_name)
            try:
                status = "@{} Hey! you found me :)".format(tweet.user.screen_name)
                api.update_status(status=status, in_reply_to_status_id=tweet.id)
            except tweepy.TweepError:
                pass
    return new_since_id


def main():
    s = open('latest.txt', 'r+')
    since_id = int(s.readline())
    while True:
        since_id = reply(since_id)
        print(since_id)
        s.seek(0)
        s.write(str(since_id))
        print("waiting ...")
        time.sleep(30)


if __name__ == '__main__':
    main()
