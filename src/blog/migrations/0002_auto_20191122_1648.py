# Generated by Django 2.2.7 on 2019-11-22 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(choices=[('901', '901'), ('902', '902')], max_length=100),
        ),
    ]
