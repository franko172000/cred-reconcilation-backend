# Generated by Django 5.1 on 2024-09-15 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('source_file', models.FileField(upload_to='uploads/')),
                ('target_file', models.FileField(upload_to='uploads/')),
                ('description', models.TextField(blank=True, null=True)),
                ('discrepancies', models.JSONField(blank=True, null=True)),
                ('missing_in_source', models.JSONField(blank=True, null=True)),
                ('missing_in_target', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'uploads',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=50)),
                ('transaction_date', models.DateField()),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.upload')),
            ],
            options={
                'db_table': 'records',
            },
        ),
    ]
