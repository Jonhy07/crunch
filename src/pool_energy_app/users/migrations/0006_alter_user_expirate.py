# Generated by Django 3.2.4 on 2021-08-25 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_expirate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expirate',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 25, 12, 21, 59, 438642)),
        ),
    ]
