# Generated by Django 2.2.6 on 2019-11-30 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_data', '0002_customer_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.CharField(max_length=255),
        ),
    ]
