# Generated by Django 2.2.7 on 2020-01-09 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('safe', '0023_auto_20191213_2109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='safe',
            options={'permissions': (('can_view', 'View This'), ('can_add', 'Add to the Safe'))},
        ),
    ]