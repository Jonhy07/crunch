# Generated by Django 2.2.20 on 2021-08-04 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0014_item_temp'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemaction',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='forms.Store'),
            preserve_default=False,
        ),
    ]
