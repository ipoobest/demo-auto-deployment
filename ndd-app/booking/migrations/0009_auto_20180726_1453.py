# Generated by Django 2.0.7 on 2018-07-26 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_auto_20180725_1801'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='pickup_form',
            new_name='pickup_from',
        ),
    ]
