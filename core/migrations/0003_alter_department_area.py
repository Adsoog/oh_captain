# Generated by Django 5.1.6 on 2025-03-04 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_siteconfig_primary_logo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.area'),
        ),
    ]
