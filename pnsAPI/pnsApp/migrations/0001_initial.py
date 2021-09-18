# Generated by Django 3.2.6 on 2021-09-15 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('userId', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=15, null=True)),
                ('password', models.CharField(max_length=400)),
                ('email', models.EmailField(max_length=200)),
                ('token', models.CharField(max_length=200)),
                ('is_activate', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='daDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boardingCheck', models.BooleanField(auto_created=True, default=False)),
                ('busStopId', models.CharField(max_length=50)),
                ('busId', models.CharField(max_length=50)),
                ('userId', models.CharField(max_length=50)),
            ],
        ),
    ]
