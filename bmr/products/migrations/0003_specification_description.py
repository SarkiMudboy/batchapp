# Generated by Django 3.2.6 on 2021-10-20 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_specification_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='specification',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
