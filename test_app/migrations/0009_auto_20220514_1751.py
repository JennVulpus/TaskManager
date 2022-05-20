# Generated by Django 2.2 on 2022-05-14 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0008_auto_20220514_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chore',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='list_chore', to='test_app.List'),
        ),
        migrations.AlterField(
            model_name='location',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='list_location', to='test_app.List'),
        ),
    ]
