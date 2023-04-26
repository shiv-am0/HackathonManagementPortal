# Generated by Django 4.2 on 2023-04-26 08:03

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hackathon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField(default=datetime.datetime.now)),
                ('end_time', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.CharField(max_length=100)),
            ],
        ),
    ]
