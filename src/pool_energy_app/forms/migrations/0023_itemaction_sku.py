# Generated by Django 2.2.20 on 2021-09-09 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0022_auto_20210908_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemaction',
            name='sku',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
