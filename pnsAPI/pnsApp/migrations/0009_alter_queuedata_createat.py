# Generated by Django 3.2.6 on 2021-10-11 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pnsApp', '0008_queuedata_createat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queuedata',
            name='createAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
