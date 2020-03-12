# Generated by Django 2.2.7 on 2020-03-12 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('components', '0014_medicunit_is_supervisor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Safe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('amount_removed', models.IntegerField(blank=True, null=True)),
                ('amount_added', models.IntegerField(blank=True, null=True)),
                ('amount_in_safe', models.IntegerField(blank=True, null=True)),
                ('incident_number', models.CharField(blank=True, default='', max_length=20)),
                ('patient_name', models.CharField(blank=True, default='', max_length=20)),
                ('free_text', models.TextField(blank=True, default='')),
                ('drug_name', models.ForeignKey(blank=True, default=0, limit_choices_to={'is_active_safe': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='drug_remove', to='components.Drug')),
                ('medic_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='medic_unit', to='components.MedicUnit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_view', 'View This'), ('can_add', 'Add to the Safe')),
            },
        ),
    ]
