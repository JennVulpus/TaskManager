# Generated by Django 3.0.4 on 2022-01-04 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_auto_20211213_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='test_app.Location'),
        ),
    ]