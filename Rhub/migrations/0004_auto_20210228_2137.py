# Generated by Django 3.0.3 on 2021-02-28 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rhub', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='probability',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='sentiment',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
