# Generated by Django 5.0.6 on 2024-06-18 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0014_alter_set_budget_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='set_budget',
            name='Electronics_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='set_budget',
            name='Grocery_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='set_budget',
            name='clothing_amoount',
            field=models.IntegerField(default=0),
        ),
    ]