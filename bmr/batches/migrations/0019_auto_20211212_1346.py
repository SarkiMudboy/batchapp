# Generated by Django 3.2.6 on 2021-12-12 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batches', '0018_auto_20211212_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchmanufacturingprocess',
            name='manufacturing_commenced',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='batchmanufacturingprocess',
            name='manufacturing_completed',
            field=models.DateField(blank=True, null=True),
        ),
    ]
