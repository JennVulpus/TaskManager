# Generated by Django 2.2 on 2022-05-14 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0007_list_group_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='list',
            name='chore',
        ),
        migrations.RemoveField(
            model_name='list',
            name='location',
        ),
        migrations.AddField(
            model_name='chore',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='test_app.List'),
        ),
        migrations.AddField(
            model_name='location',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='test_app.List'),
        ),
    ]
