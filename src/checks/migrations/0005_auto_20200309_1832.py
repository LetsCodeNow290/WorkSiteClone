# Generated by Django 2.2.7 on 2020-03-09 18:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checks', '0004_auto_20200309_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rsibag',
            name='next_expiration_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
