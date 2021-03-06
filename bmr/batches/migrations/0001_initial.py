# Generated by Django 3.2.6 on 2021-08-30 19:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('staff', '0001_initial'),
        ('rawmaterials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.CharField(max_length=20)),
                ('gross_weight', models.FloatField(blank=True, help_text='in kilograms', null=True)),
                ('net_weight', models.FloatField(blank=True, help_text='in kilograms', null=True)),
                ('manufacturing_date', models.DateField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('batch_size', models.IntegerField(blank=True, null=True)),
                ('percentage_yield', models.IntegerField(blank=True, help_text='in percentage', null=True)),
                ('expected_yield', models.IntegerField(blank=True, help_text='in percentage', null=True)),
                ('actual_yield', models.FloatField(blank=True, null=True)),
                ('pack_size', models.IntegerField(blank=True, null=True)),
                ('production_commencement', models.DateField(blank=True, null=True)),
                ('production_completion', models.DateField(blank=True, null=True)),
                ('release_status', models.BooleanField(blank=True, default=False, null=True)),
                ('yield_deviation_limit', models.FloatField(blank=True, help_text='+/-', null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='BatchManufacturingProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_from', models.DateTimeField(blank=True, null=True)),
                ('action_to', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batchmanufacturingprocess_action_by', to='staff.staff')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batchmanufacturingprocess_checked_by', to='staff.staff')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.manufacturingprocess')),
            ],
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard_instructions', models.TextField(max_length=8000)),
                ('issuance', models.TextField(max_length=8000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PackagingMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=100)),
                ('dimension', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(blank=True, null=True)),
                ('id_complies', models.BooleanField(blank=True, null=True)),
                ('result_type', models.CharField(choices=[('CHM', 'CHEMICAL'), ('MCR', 'MICRO')], max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.test')),
            ],
        ),
        migrations.CreateModel(
            name='ReleaseProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.CharField(max_length=100)),
                ('analytical_result', models.BooleanField(default=False)),
                ('remark', models.TextField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='releaseprofile_checked_by', to='staff.staff')),
                ('quality_assurance_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='releaseprofile_qa_manager', to='staff.staff')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.test')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterialPackagingBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_dispensed', models.IntegerField(blank=True, help_text='in kilograms', null=True)),
                ('dispensed_to', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rawmaterialpackagingbill_action_by', to='staff.staff')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rawmaterialpackagingbill_checked_by', to='staff.staff')),
                ('dispense_label_auth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rawmaterialpackagingbill_auth_by', to='staff.staff')),
                ('raw_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rawmaterials.rawmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterialCheckRecordAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rawmaterialcheckrecordauth_assignment', to='staff.staff')),
                ('batch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('check_done_by', models.ManyToManyField(blank=True, null=True, to='staff.Staff')),
                ('total_assignment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rawmaterialcheckrecordauth_total_assignment', to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterialCheckRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_tested', models.DateField(blank=True, null=True)),
                ('result', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rawmaterialcheckrecord_checked_by', to='staff.staff')),
                ('raw_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rawmaterials.rawmaterialbatch')),
                ('weighed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rawmaterialcheckrecord_weighed_by', to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterialBillAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rawmaterialbillauth_approved_by', to='staff.staff')),
                ('batch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('confirmed_by', models.ManyToManyField(blank=True, to='staff.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='QualityControlAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ar_number', models.CharField(max_length=50)),
                ('pharmacopiea_specification_year', models.DateField(blank=True, null=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('chemical_analyst', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualitycontrolanalysis_chemical_analyst', to='staff.staff')),
                ('microbiologist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualitycontrolanalysis_microbiologist', to='staff.staff')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('quality_control_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualitycontrolanalysis_QC_manager', to='staff.staff')),
                ('result_pharmacopiea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.specification')),
                ('results', models.ManyToManyField(blank=True, null=True, to='batches.TestResult')),
            ],
        ),
        migrations.CreateModel(
            name='ProductReconciliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.TextField(max_length=100)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('sales_quantity', models.CharField(max_length=100)),
                ('remarks', models.TextField(max_length=50)),
                ('quantity_supplied', models.IntegerField(blank=True, null=True)),
                ('quantity_damaged', models.IntegerField(blank=True, null=True)),
                ('quantity_rejected', models.IntegerField(blank=True, null=True)),
                ('quantity_returned', models.IntegerField(blank=True, null=True)),
                ('quantity_used', models.IntegerField(blank=True, null=True)),
                ('percentage_breakage', models.FloatField(blank=True, help_text='in percentage', null=True)),
                ('percentage_damages', models.FloatField(blank=True, help_text='in percentage', null=True)),
                ('deviation', models.FloatField(blank=True, help_text='+/- (%)', null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('pack_sizes', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('collected_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productreconciliation_approved_by', to='staff.staff')),
                ('issued_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productreconciliation_issued_by', to='staff.staff')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.packagingmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='InprocessAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('action_by', models.ManyToManyField(blank=True, null=True, related_name='inprocessauth_action_by', to='staff.Staff')),
                ('batch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ManyToManyField(blank=True, null=True, related_name='inprocessauth_checked_by', to='staff.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='IndividualWieght',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.CharField(blank=True, max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentClearance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check', models.TextField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_approved_by', to='staff.staff')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_checked_by', to='staff.staff')),
                ('cleaned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_cleaned_by', to='staff.staff')),
                ('last_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_last_product', to='products.product')),
                ('next_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_next_product', to='products.product')),
                ('quality_assurance_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentclearance_qa_manager', to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentcheck_action_by', to='staff.staff')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentcheck_checked_by', to='staff.staff')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.equipment')),
                ('last_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipmentcheck_last_product', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='ControlRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(max_length=50)),
                ('result', models.FloatField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
            ],
        ),
        migrations.CreateModel(
            name='CleaningProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_description', models.TextField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cleaningprocess_action_by', to='staff.staff')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cleaningprocess_checked_by', to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='BillOfPackaging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_required', models.IntegerField(blank=True, null=True)),
                ('actual_quantity', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billofpackaging_action_by', to='staff.staff')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billofpackaging_checked_by', to='staff.staff')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.packagingmaterial')),
            ],
        ),
        migrations.CreateModel(
            name='BatchPackagingProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.TextField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batchpackagingprocess_action_by', to='staff.staff')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batchpackagingprocess_checked_by', to='staff.staff')),
            ],
        ),
        migrations.CreateModel(
            name='BatchPackagingAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batchpackagingauth_approved_by', to='staff.staff')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batches.batch')),
                ('confirmed_by', models.ManyToManyField(to='staff.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='BatchManufacturingProcessAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturing_commenced', models.DateField()),
                ('manufacturing_completed', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('process', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='batches.batchmanufacturingprocess')),
                ('production_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batchmanufacturingprocessauth_production_manager', to='staff.staff')),
            ],
        ),
    ]
