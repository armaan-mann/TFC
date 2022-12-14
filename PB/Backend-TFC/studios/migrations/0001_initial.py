# Generated by Django 4.1.3 on 2022-11-20 01:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, default=0, max_digits=9)),
                ('postal_code', models.CharField(max_length=7)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, upload_to='studio_images/')),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Image', to='studios.studio')),
            ],
        ),
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default=None, max_length=30)),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ammenity', to='studios.studio')),
            ],
        ),
        migrations.AddConstraint(
            model_name='amenities',
            constraint=models.UniqueConstraint(fields=('studio', 'type'), name='unique_type'),
        ),
    ]
