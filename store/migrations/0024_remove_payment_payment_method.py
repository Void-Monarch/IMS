# Generated by Django 4.2.3 on 2023-09-12 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_payment_payment_method_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
    ]
