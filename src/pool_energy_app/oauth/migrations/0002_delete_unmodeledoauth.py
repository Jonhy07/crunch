# Generated by Django 2.2.6 on 2021-01-14 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UnmodeledOauth',
        ),
    ]
