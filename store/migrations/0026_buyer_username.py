# Generated by Django 4.2.3 on 2023-09-13 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_rename_name_buyer_first_name_buyer_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='username',
            field=models.CharField(default=1, max_length=120, unique=True),
            preserve_default=False,
        ),
    ]
