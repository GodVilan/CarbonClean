# Generated by Django 5.1.3 on 2024-11-11 17:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarbonEmission', '0005_alter_useractivity_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 11, 10, 0, 0)),
            preserve_default=False,
        ),
    ]