# Generated by Django 2.2.6 on 2019-12-09 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redditors', '0002_redditor_num_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redditor',
            name='num_friends',
            field=models.PositiveIntegerField(default=0, help_text='Count of friends.', null=True, verbose_name='friends count'),
        ),
    ]