# Generated by Django 4.2.3 on 2023-09-17 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_buyer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_quantity',
            field=models.PositiveIntegerField(default=1, max_length=16),
        ),
    ]
