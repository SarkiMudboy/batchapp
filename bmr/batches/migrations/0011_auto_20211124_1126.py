# Generated by Django 3.2.6 on 2021-11-24 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_manufacturingprocess_step'),
        ('staff', '0001_initial'),
        ('batches', '0010_auto_20211122_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentclearance',
            name='last_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_last_product', to='products.product'),
        ),
        migrations.AddField(
            model_name='equipmentclearance',
            name='next_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_next_product', to='products.product'),
        ),
        migrations.AddField(
            model_name='equipmentclearance',
            name='quality_assurance_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_qa_manager', to='staff.staff'),
        ),
        migrations.DeleteModel(
            name='EQClearanceAuth',
        ),
    ]
