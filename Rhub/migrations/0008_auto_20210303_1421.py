# Generated by Django 3.0.3 on 2021-03-03 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rhub', '0007_auto_20210301_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
