# Generated by Django 2.2.7 on 2019-11-20 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('safe', '0002_auto_20191120_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='safeadd',
            old_name='drug_add',
            new_name='drug_name',
        ),
        migrations.RenameField(
            model_name='saferemove',
            old_name='drug_remove',
            new_name='drug_name',
        ),
    ]
