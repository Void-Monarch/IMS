# Generated by Django 4.2.3 on 2023-09-05 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_order_total'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InvoiceDetail',
            new_name='InvoiceDetails',
        ),
    ]
