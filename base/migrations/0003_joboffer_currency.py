# Generated by Django 4.0.3 on 2022-04-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_name_company_company_name_alter_company_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='joboffer',
            name='currency',
            field=models.TextField(default='PLN'),
        ),
    ]