# Generated by Django 3.2.6 on 2021-12-12 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batches', '0017_batchmanufacturingprocess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchmanufacturingprocess',
            name='action_from',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='batchmanufacturingprocess',
            name='action_to',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
