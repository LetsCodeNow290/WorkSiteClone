# Generated by Django 2.2.7 on 2019-12-13 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('safe', '0020_auto_20191213_2058'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='safe',
            options={'permissions': (('can_view', 'Can view the safe'),)},
        ),
    ]
