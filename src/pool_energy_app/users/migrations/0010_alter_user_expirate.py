# Generated by Django 3.2.4 on 2021-09-09 00:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_expirate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expirate',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 9, 0, 6, 22, 70350)),
        ),
    ]
