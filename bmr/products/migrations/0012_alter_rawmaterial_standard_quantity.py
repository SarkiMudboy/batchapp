# Generated by Django 3.2.6 on 2021-12-12 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_manufacturingprocess_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawmaterial',
            name='standard_quantity',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
