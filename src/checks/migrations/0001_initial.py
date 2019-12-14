# Generated by Django 2.2.7 on 2019-12-13 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('components', '0011_auto_20191204_1645'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RSIBag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateTimeField(auto_now=True)),
                ('seal_number', models.IntegerField()),
                ('incident_number', models.CharField(max_length=20)),
                ('hospital', models.CharField(max_length=50)),
                ('contact_EMS_Chief_date_and_time', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NarcBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateTimeField(auto_now=True)),
                ('seal_number', models.IntegerField()),
                ('incident_number', models.CharField(max_length=20)),
                ('hospital', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateTimeField(auto_now=True)),
                ('emergency_lights', models.BooleanField()),
                ('driving_lights', models.BooleanField()),
                ('red_bag', models.BooleanField()),
                ('LP_15', models.BooleanField()),
                ('BLS_bag', models.BooleanField()),
                ('RTF_bag', models.BooleanField()),
                ('Suction', models.BooleanField()),
                ('oxygen', models.BooleanField()),
                ('medic_unit_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medic_unit_number', to='components.MedicUnit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]