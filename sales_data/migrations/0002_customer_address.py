# Generated by Django 2.2.6 on 2019-11-30 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(default=12, max_length=255),
            preserve_default=False,
        ),
    ]
