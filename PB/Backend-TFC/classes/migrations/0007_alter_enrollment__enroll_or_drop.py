# Generated by Django 4.1.3 on 2022-12-03 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_alter_enrollment__enroll_or_drop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='_enroll_or_drop',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
