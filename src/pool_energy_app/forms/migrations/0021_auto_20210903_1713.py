# Generated by Django 2.2.20 on 2021-09-03 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0020_item_temp_marketplace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='costo',
            field=models.FloatField(null=True),
        ),
    ]
