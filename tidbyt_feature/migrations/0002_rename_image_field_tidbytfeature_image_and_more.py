# Generated by Django 4.0 on 2022-01-03 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tidbyt_feature', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tidbytfeature',
            old_name='image_field',
            new_name='image',
        ),
        migrations.AddField(
            model_name='tidbytfeature',
            name='text',
            field=models.TextField(blank=True),
        ),
    ]
