# Generated by Django 2.2.6 on 2019-11-24 17:44

from django.db import migrations
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191124_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientorg',
            name='reddit_token',
            field=encrypted_model_fields.fields.EncryptedCharField(help_text='Reddit refresh token for the Salesforce Client Org.', null=True),
        ),
    ]
