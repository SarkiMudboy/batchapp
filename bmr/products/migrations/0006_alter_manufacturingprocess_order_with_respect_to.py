# Generated by Django 3.2.6 on 2021-11-08 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20211106_1914'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='manufacturingprocess',
            order_with_respect_to='product',
        ),
    ]
