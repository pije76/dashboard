# Generated by Django 2.2.6 on 2019-12-11 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_data', '0011_auto_20191211_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopviewchannel',
            name='land',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='product_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
