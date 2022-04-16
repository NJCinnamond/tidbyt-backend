# Generated by Django 4.0 on 2022-01-05 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tidbyt_installation', '0002_tidbytinstallation_installation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='tidbytinstallation',
            name='install_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tidbytinstallation',
            name='uninstall_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]