# Generated by Django 3.0.3 on 2021-03-17 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rhub', '0011_auto_20210317_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='subject',
            field=models.CharField(max_length=100),
        ),
    ]
