# Generated by Django 3.2.6 on 2021-11-16 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('batches', '0004_auto_20211115_1016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batchinfoauth',
            name='product',
        ),
        migrations.AlterField(
            model_name='batchinfoauth',
            name='batch',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='batches.batch'),
        ),
    ]
