# Generated by Django 4.0.3 on 2022-04-04 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_joboffer_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='joboffer',
            old_name='location',
            new_name='city',
        ),
    ]
