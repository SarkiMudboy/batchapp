# Generated by Django 3.2.6 on 2021-11-05 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_specification_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturingprocess',
            name='substep',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
