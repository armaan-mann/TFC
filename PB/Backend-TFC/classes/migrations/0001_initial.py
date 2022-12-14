# Generated by Django 4.1.3 on 2022-11-20 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('coach', models.CharField(max_length=100)),
                ('keywords', models.TextField()),
                ('capacity', models.PositiveIntegerField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('start_recursion', models.DateField()),
                ('end_recursion', models.DateField()),
                ('studio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studios.studio')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_start_time', models.TimeField(blank=True, null=True)),
                ('_start_recursion', models.DateField(blank=True, null=True)),
                ('enroll_or_drop', models.CharField(choices=[['False', 'Enroll'], ['False', 'Drop'], ['False', 'Drop_All'], ['False', 'Enroll_ALL']], max_length=10, null=True)),
                ('enrolled', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.class')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClassHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_status', models.CharField(blank=True, max_length=10, null=True)),
                ('_name', models.CharField(max_length=100)),
                ('_coach', models.CharField(max_length=100)),
                ('_keywords', models.TextField()),
                ('start_Time', models.TimeField()),
                ('end_Time', models.TimeField()),
                ('start_Recursion', models.DateField()),
                ('end_Recursion', models.DateField()),
                ('_studio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studios.studio')),
                ('_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.enrollment')),
            ],
        ),
    ]
