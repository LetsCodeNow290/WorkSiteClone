# Generated by Django 2.2.7 on 2019-11-22 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0009_auto_20191121_0843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drug',
            name='concentration',
        ),
    ]
