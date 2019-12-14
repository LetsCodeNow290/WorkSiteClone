# Generated by Django 2.2.7 on 2019-12-04 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0010_remove_drug_concentration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drug',
            old_name='is_active',
            new_name='is_active_safe',
        ),
        migrations.AddField(
            model_name='drug',
            name='is_active_unit',
            field=models.BooleanField(default=True),
        ),
    ]