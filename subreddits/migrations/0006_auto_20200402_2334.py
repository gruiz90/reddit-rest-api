# Generated by Django 2.2.6 on 2020-04-02 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subreddits', '0005_auto_20191204_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subreddit',
            name='public_description',
            field=models.TextField(blank=True, help_text='Description of the subreddit, shown in searches and on the "You must be invited to visit this community" page(if applicable).', null=True),
        ),
    ]
