# Generated by Django 5.0.6 on 2024-06-15 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0013_alter_set_budget_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set_budget',
            name='month',
            field=models.IntegerField(default=6),
        ),
    ]
