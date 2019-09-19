import praw
import random
import config

# reddit auth
reddit_clientId = config.reddit_clientId
reddit_clientSecret = config.reddit_clientSecret
user_agent = config.user_agent

# reddit object
reddit = praw.Reddit(client_id=reddit_clientId,
                     client_secret=reddit_clientSecret,
                     user_agent=user_agent)


def interesting():
    list_of_subreddits = ['interestingasfuck', 'Damnthatsinteresting', 'BeAmazed']
    sr = random.choice(list_of_subreddits)
    list_of_submissions = []
    for submission in reddit.subreddit(sr).top(limit=10):
        sub = {'title': submission.title, 'url': submission.url}
        list_of_submissions.append(sub)
    return random.choice(list_of_submissions)
