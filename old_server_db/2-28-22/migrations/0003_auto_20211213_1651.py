# Generated by Django 2.2 on 2021-12-13 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_auto_20211213_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='done_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chore',
            name='renew_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
