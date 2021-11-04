# Generated by Django 3.2.4 on 2021-07-26 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('endpoint', '0001_initial'),
        ('charts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('column', models.IntegerField()),
                ('finish', models.BooleanField(default=False)),
                ('send', models.JSONField(null=True)),
                ('endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Endpoint', to='endpoint.endpoint')),
                ('row', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Row', to='charts.row')),
            ],
        ),
        migrations.CreateModel(
            name='Type_agrupation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Type_calculate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Type_graph',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='YRow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Graph', to='graphs.graph')),
                ('type_calculate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Type_calculate', to='graphs.type_calculate')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Detail_Y', to='endpoint.detail')),
            ],
        ),
        migrations.AddField(
            model_name='graph',
            name='type_agrupation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Type_agrupation', to='graphs.type_agrupation'),
        ),
        migrations.AddField(
            model_name='graph',
            name='type_graph',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Type_graph', to='graphs.type_graph'),
        ),
        migrations.AddField(
            model_name='graph',
            name='xrow',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Detail_X', to='endpoint.detail'),
        ),
    ]
