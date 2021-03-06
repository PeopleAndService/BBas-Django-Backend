# Generated by Django 3.2.6 on 2021-10-09 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pnsApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='busStationData',
            fields=[
                ('nodeId', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('stationName', models.CharField(max_length=30)),
                ('cityCode', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='DriverAccount',
            fields=[
                ('did', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('pushToken', models.CharField(max_length=255, null=True)),
                ('pushSetting', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('vehicleId', models.CharField(max_length=50, null=True)),
                ('busRouteId', models.CharField(max_length=20, null=True)),
                ('cityCode', models.IntegerField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PassengerAccount',
            fields=[
                ('uid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('pushToken', models.CharField(max_length=255, null=True)),
                ('pushSetting', models.BooleanField(default=False)),
                ('emergencyPhone', models.CharField(max_length=13, null=True)),
                ('cityCode', models.IntegerField(max_length=20, null=True)),
                ('lfBusOption', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QueueData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stbusStopId', models.CharField(max_length=50)),
                ('edbusStopId', models.CharField(max_length=50)),
                ('vehicleId', models.CharField(max_length=50)),
                ('busRouteId', models.CharField(max_length=20)),
                ('boardingCheck', models.BooleanField(default=False)),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, related_name='user_data', to='pnsApp.passengeraccount')),
            ],
        ),
        migrations.CreateModel(
            name='RatingData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ratingData', models.FloatField(max_length=5)),
                ('did', models.ForeignKey(db_column='did', on_delete=django.db.models.deletion.CASCADE, related_name='rated', to='pnsApp.driveraccount')),
            ],
        ),
        migrations.CreateModel(
            name='routeData',
            fields=[
                ('busRouteId', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('destination', models.CharField(max_length=30)),
                ('routeNo', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='routePerBus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lfBus', models.CharField(max_length=20)),
                ('busRouteId', models.ForeignKey(db_column='busRouteId', on_delete=django.db.models.deletion.CASCADE, related_name='Stations_route', to='pnsApp.routedata')),
                ('nodeId', models.ForeignKey(db_column='nodeId', on_delete=django.db.models.deletion.CASCADE, related_name='Stations_route', to='pnsApp.busstationdata')),
            ],
        ),
        migrations.DeleteModel(
            name='Account',
        ),
        migrations.DeleteModel(
            name='daDB',
        ),
    ]
