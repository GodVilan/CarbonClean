# Generated by Django 5.1.3 on 2024-12-04 02:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarbonEmission', '0010_subcategoryeffect_subcategorysolution'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StepSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='CarbonEmission.stepcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='CarbonEmission.stepsubcategory')),
            ],
        ),
    ]
