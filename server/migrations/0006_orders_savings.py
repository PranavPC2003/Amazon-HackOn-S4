# Generated by Django 5.0.6 on 2024-06-14 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_rename_items_list_orders_order_items_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='savings',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]