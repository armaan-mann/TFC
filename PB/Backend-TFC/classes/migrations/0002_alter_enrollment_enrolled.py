# Generated by Django 4.1.3 on 2022-11-20 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='enrolled',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='classes.class'),
        ),
    ]