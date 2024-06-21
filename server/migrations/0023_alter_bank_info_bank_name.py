# Generated by Django 5.0.6 on 2024-06-21 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0022_alter_bank_info_bank_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank_info',
            name='bank_name',
            field=models.CharField(blank=True, choices=[('SBI', 'State Bank of India'), ('HDFC', 'HDFC Bank'), ('ICICI', 'ICICI Bank'), ('KOTAK', 'Kotak Bank'), ('AMEX', 'American Express Bank'), ('PAYTM', 'Paytm'), ('PhonePe', 'PhonePe UPI'), ('Amazon Pay', 'Amazon Pay UPI'), ('CASH', 'Cash'), ('PAYTM Wallet', 'Paytm Wallet'), ('PhonePe Wallet', 'PhonePe Wallet'), ('Amazon Wallet', 'Amazon Pay Wallet')], max_length=30, null=True),
        ),
    ]
