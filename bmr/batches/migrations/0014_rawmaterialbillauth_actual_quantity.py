# Generated by Django 3.2.6 on 2021-11-24 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batches', '0013_auto_20211124_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawmaterialbillauth',
            name='actual_quantity',
            field=models.IntegerField(blank=True, help_text='in kilograms or gram mil', null=True),
        ),
    ]
