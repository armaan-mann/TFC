# Generated by Django 4.1.3 on 2022-12-03 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0005_remove_class_is_active_enrollment__is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='_enroll_or_drop',
            field=models.CharField(choices=[['False', 'enroll'], ['False', 'drop'], ['False', 'drop_all'], ['False', 'enroll_all']], max_length=10, null=True),
        ),
    ]
