# Generated by Django 2.2.7 on 2019-12-13 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safe', '0016_auto_20191204_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='safe',
            name='free_text',
            field=models.TextField(blank=True, default='None'),
        ),
        migrations.AlterField(
            model_name='safe',
            name='incident_number',
            field=models.CharField(blank=True, default='None', max_length=20),
        ),
        migrations.AlterField(
            model_name='safe',
            name='patient_name',
            field=models.CharField(blank=True, default='None', max_length=20),
        ),
    ]
