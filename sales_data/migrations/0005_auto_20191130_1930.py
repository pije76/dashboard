# Generated by Django 2.2.6 on 2019-11-30 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_data', '0004_auto_20191130_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(),
        ),
    ]
