from django.db import models
import uuid
import praw


class Subreddit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    display_name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    public_description = models.CharField(max_length=256)
    created_utc = models.BigIntegerField()
    subscribers = models.PositiveIntegerField('subscribers count')
    over18 = models.BooleanField('NSFW')

    def __str__(self):
        return f"Subreddit name: {self.name}\n"
        f"Description: {self.description}\nTotal subs: {self.subscribers}"

    def get_or_create_by_name(self, name):
        pass
        # subreddit = Subreddit.
        # reddit = praw.Reddit(client_id=Env.str('REDDIT_CLIENT_ID'),
    #                client_secret=Env.str('REDDIT_CLIENT_SECRET'),
    #                user_agent=Env.str('REDDIT_USER_AGENT'))
        # subreddit = reddit.subreddit(name)
        # return subreddit
