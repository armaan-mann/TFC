# Generated by Django 4.1.3 on 2022-12-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studio',
            name='distance',
            field=models.CharField(blank=True, default=0, max_length=40, null=True),
        ),
    ]
