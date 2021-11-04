# Generated by Django 2.2.20 on 2021-04-16 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0010_userstore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homologation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item1', to='forms.Item')),
                ('item2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item2', to='forms.Item')),
            ],
        ),
    ]
