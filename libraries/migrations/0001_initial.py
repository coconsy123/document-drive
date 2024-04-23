# Generated by Django 5.0.3 on 2024-03-19 03:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'tbl_categorytype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DivisionType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'tbl_divisiontype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'tbl_documenttype',
                'managed': False,
            },
        ),
    ]