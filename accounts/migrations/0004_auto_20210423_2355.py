# Generated by Django 3.1 on 2021-04-23 18:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210423_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activation_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 23, 23, 55, 20, 474594)),
        ),
    ]
